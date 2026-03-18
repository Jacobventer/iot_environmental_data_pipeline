import pandas as pd
from pymongo import MongoClient
import os
import logging
import time

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

for attempt in range(3):
    try:
        client = MongoClient(mongo_uri)
        db = client["iot_environment"]
        collection = db["sensor_readings"]
        logging.info("Connected to MongoDB")
        break
    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
        time.sleep(2)

db = client["iot_environment"]
collection = db["sensor_readings"]

logging.info("Starting data load")

#Clear existing data
collection.delete_many({})
print("Existing data cleared.")
logging.info("Existing data cleared")

#Load CSV
file_path = "data/iot_telemetry_data.csv"
df = pd.read_csv(file_path)

print(f"Loaded {len(df)} rows from CSV.")
logging.info(f"Loaded {len(df)} rows from CSV")

#Convert dataframe to dictionary records
data = df.to_dict(orient="records")

#Insert in batches
batch_size = 10000

for i in range(0, len(data), batch_size):
    batch = data[i:i + batch_size]
    collection.insert_many(batch)
    print(f"Inserted batch {i // batch_size + 1}")

logging.info("Data loading completed")

print("Data loading completed successfully.")
total = collection.count_documents({})
print(f"Total records in MongoDB: {total}")
logging.info(f"Total records in MongoDB: {total}")
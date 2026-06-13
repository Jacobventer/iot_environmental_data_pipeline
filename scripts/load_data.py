"""
Load IoT telemetry data into MongoDB using batch processing.

This script loads environmental sensor data from CSV in batches, 
validates records, inserts data into MongoDB using chunk loading, and
creates batch progress and system health outputs.

Outputs
-------
batch_status.json
    Tracks batch progress and loading status.

system_health.json
    Reports pipeline and data-quality health.
"""

import pandas as pd
from pymongo import MongoClient
import os
import logging
import time
import json
from datetime import datetime

os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

failed_batches = 0
invalid_records = 0

for attempt in range(3):

    try:
        client = MongoClient(mongo_uri)
        db = client["iot_environment"]
        collection = db["sensor_readings"]
        logging.info("Connected to MongoDB")
        mongo_status = "connected"
        break

    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
        mongo_status = "failed"
        time.sleep(5)

db = client["iot_environment"]
collection = db["sensor_readings"]

logging.info("Starting data load")

#Clear existing data
collection.delete_many({})
print("Existing data cleared.")
logging.info("Existing data cleared")

#Load CSV
file_path = "data/iot_telemetry_data.csv"

#Insert in batches using chunk loading
batch_size = 10000
total_loaded = 0

for batch_number, chunk in enumerate(pd.read_csv(file_path, chunksize=batch_size)):

    #Validate records
    valid_chunk = chunk.dropna(subset=["temp", "smoke", "co"])

    invalid_in_batch = len(chunk) - len(valid_chunk)
    invalid_records += invalid_in_batch

    if invalid_in_batch > 0:
        logging.warning(f"Batch {batch_number + 1}: {invalid_in_batch} invalid records skipped")

    #Convert dataframe to dictionary records
    data = valid_chunk.to_dict(orient="records")

    try:

        #Insert batch
        collection.insert_many(data)

        total_loaded += len(data)

        #Batch progress tracking
        batch_status = {
            "last_batch": batch_number + 1,
            "records_loaded": total_loaded,
            "status": "running"
        }

        with open("output/batch_status.json", "w") as f:
            json.dump(batch_status, f, indent=4)

        print(f"Inserted batch {batch_number + 1} ({len(data)} valid records)")
        logging.info(f"Inserted batch {batch_number + 1} ({len(data)} valid records)")

    except Exception as e:
        failed_batches += 1
        logging.error(f"Batch {batch_number + 1} failed: {e}")

logging.info("Data loading completed")

total = collection.count_documents({})

#Final batch status
batch_status = {
    "last_batch": batch_number + 1,
    "records_loaded": total,
    "status": "completed"
}

with open("output/batch_status.json", "w") as f:
    json.dump(batch_status, f, indent=4)

#System health monitoring
system_health = {
    "pipeline_status": "healthy" if failed_batches == 0 else "warning",
    "mongodb_connection": mongo_status,
    "failed_batches": failed_batches,
    "invalid_records": invalid_records,
    "last_successful_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open("output/system_health.json", "w") as f:
    json.dump(system_health, f, indent=4)

print("Data loading completed successfully.")
print(f"Total records in MongoDB: {total}")
print(f"Invalid records skipped: {invalid_records}")

logging.info(f"Total records in MongoDB: {total}")
logging.info(f"Invalid records skipped: {invalid_records}")
logging.info(f"System health: {system_health}")
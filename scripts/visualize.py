from pymongo import MongoClient
import os
import matplotlib.pyplot as plt

#Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

db = client["iot_environment"]
collection = db["sensor_readings"]

print("Connected to MongoDB for visualization.")

#Load data
data = list(collection.find())

#Extract values
temps = [d.get("temp", 0) for d in data]
smoke = [d.get("smoke", 0) for d in data]
co = [d.get("co", 0) for d in data]

#Thresholds
TEMP_HIGH = 30.4
TEMP_LOW = 11
SMOKE_HIGH = 0.042
CO_HIGH = 0.012

os.makedirs("output", exist_ok=True)

#Temperature distribution
plt.figure()
plt.hist(temps, bins=50)
plt.axvline(TEMP_HIGH, linestyle='--')
plt.axvline(TEMP_LOW, linestyle='--')
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.savefig("output/temp_distribution.png")

#Smoke distribution
plt.figure()
plt.hist(smoke, bins=50)
plt.axvline(SMOKE_HIGH, linestyle='--')
plt.title("Smoke Distribution")
plt.xlabel("Smoke")
plt.ylabel("Frequency")
plt.savefig("output/smoke_distribution.png")

#CO pdistribution
plt.figure()
plt.hist(co, bins=50)
plt.axvline(CO_HIGH, linestyle='--')
plt.title("CO Distribution")
plt.xlabel("CO")
plt.ylabel("Frequency")
plt.savefig("output/co_distribution.png")

print("Distribution plots saved.")
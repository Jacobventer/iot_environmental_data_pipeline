from pymongo import MongoClient
import os
import json
import logging

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

db = client["iot_environment"]
collection = db["sensor_readings"]

print("Connected to MongoDB for analysis.")


#Thersholds

TEMP_HIGH = 30.4
TEMP_LOW = 11
SMOKE_HIGH = 0.042
CO_HIGH = 0.012


#Load data
data = list(collection.find()) 


#Init structures 
alerts = []

counts = {
    "high_temp": 0,
    "low_temp": 0,
    "high_smoke": 0,
    "high_co": 0
}

temps = []
smokes = []
cos = []


#Process data
for record in data:
    sensor = record.get("device", "unknown")

    temp = record.get("temp", 0)
    smoke = record.get("smoke", 0)
    co = record.get("co", 0)

    temps.append(temp)
    smokes.append(smoke)
    cos.append(co)

    #Temperature alerts
    if temp > TEMP_HIGH:
        counts["high_temp"] += 1
        alerts.append({"sensor": sensor, "type": "high_temp", "value": temp})

    if temp < TEMP_LOW:
        counts["low_temp"] += 1
        alerts.append({"sensor": sensor, "type": "low_temp", "value": temp})

    # Smoke alerts
    if smoke > SMOKE_HIGH:
        counts["high_smoke"] += 1
        alerts.append({"sensor": sensor, "type": "high_smoke", "value": smoke})

    # CO alerts
    if co > CO_HIGH:
        counts["high_co"] += 1
        alerts.append({"sensor": sensor, "type": "high_co", "value": co})


#Summary stats
summary = {
    "temperature": {
        "avg": sum(temps)/len(temps),
        "max": max(temps),
        "min": min(temps)
    },
    "smoke": {
        "avg": sum(smokes)/len(smokes),
        "max": max(smokes)
    },
    "co": {
        "avg": sum(cos)/len(cos),
        "max": max(cos)
    }
}

logging.info("Starting analysis")
logging.info(f"Total alerts: {len(alerts)}")
logging.info(f"Warning counts: {counts}")
logging.info("Analysis completed")
logging.info("Visualization completed")

#Save outputs
os.makedirs("output", exist_ok=True)

with open("output/alerts.json", "w") as f:
    json.dump(alerts, f, indent=4)

with open("output/warning_counts.json", "w") as f:
    json.dump(counts, f, indent=4)

with open("output/summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("Analysis completed.")
print(f"Alerts: {len(alerts)}")
print(f"Counts: {counts}")



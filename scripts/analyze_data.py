"""
Analyse environmental sensor data and generate municipal outputs.

This script loads sensor data from MongoDB, validates readings,
generates alerts, computes summary statistics and creates
planner-facing outputs.

Outputs
-------
alerts.json
    Individual sensor alerts.

warning_counts.json
    Counts of threshold breaches.

summary.json
    Statistical summaries.

municipal_report.json
    Planner-facing information service output.
"""

from pymongo import MongoClient
import os
import json
import logging

os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(mongo_uri)

db = client["iot_environment"]
collection = db["sensor_readings"]

print("Connected to MongoDB for analysis.")

#Thresholds
TEMP_HIGH = 30.4
TEMP_LOW = 11
SMOKE_HIGH = 0.042
CO_HIGH = 0.012

#Load data in batches
cursor = collection.find()

#Init structures
alerts = []

counts = {"high_temp": 0, "low_temp": 0, "high_smoke": 0, "high_co": 0}

temps = []
smokes = []
cos = []

invalid_records = 0

#Process mongo cursor
for record in cursor:

    sensor = record.get("device", "unknown")

    temp = record.get("temp")
    smoke = record.get("smoke")
    co = record.get("co")

    #Validate missing values
    if temp is None or smoke is None or co is None:
        invalid_records += 1

        logging.warning(f"Invalid record skipped for "  f"sensor {sensor}")
        continue

    temps.append(temp)
    smokes.append(smoke)
    cos.append(co)

    # Temperature alerts
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
        "avg": sum(temps) / len(temps),
        "max": max(temps),
        "min": min(temps)
    },
    "smoke": {
        "avg": sum(smokes) / len(smokes),
        "max": max(smokes)
    },
    "co": {
        "avg": sum(cos) / len(cos),
        "max": max(cos)
    }
}

#Municipal information service
total_alerts = len(alerts)

if invalid_records > 0:
    service_status = "warning"

    planner_message = ("Data quality issue detected. " "Some sensor values were missing.")

    recommended_action = ("Review sensor quality and " "monitor incoming data.")

elif total_alerts > 0:
    service_status = "warning"

    planner_message = ("Environmental warnings detected.")

    recommended_action = ("Review alert areas and continue " "environmental monitoring.")

else:
    service_status = "healthy"

    planner_message = ("Environmental conditions stable.")

    recommended_action = ("Continue routine monitoring.")

municipal_report = {
    "service_status": service_status,
    "planner_message": planner_message,
    "alerts_detected": total_alerts,
    "invalid_records": invalid_records,
    "recommended_action": recommended_action
}

logging.info("Starting analysis")
logging.info(f"Total alerts: {len(alerts)}")
logging.info(f"Warning counts: {counts}")
logging.info(
    f"Invalid records: {invalid_records}"
)
logging.info("Analysis completed")

#Save outputs
with open(
    "output/alerts.json",
    "w"
) as f:
    json.dump(alerts, f, indent=4)

with open("output/warning_counts.json", "w") as f:
    json.dump(counts, f, indent=4)

with open("output/summary.json", "w") as f:
    json.dump(summary, f, indent=4)

with open("output/municipal_report.json", "w") as f:
    json.dump(municipal_report, f, indent=4)

print("Analysis completed.")
print(f"Alerts: {len(alerts)}")
print(f"Counts: {counts}")
print(f"Invalid records: " f"{invalid_records}")
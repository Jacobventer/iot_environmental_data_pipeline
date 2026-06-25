"""
Generate environmental visualisations and municipal dashboard.

This script creates sensor distribution plots and a simple
municipal information dashboard for planners.

Outputs
-------
temp_distribution.png
smoke_distribution.png
co_distribution.png
municipal_dashboard.html
"""

from pymongo import MongoClient
import matplotlib.pyplot as plt
import os
import json
from collections import Counter

os.makedirs("output", exist_ok=True)

#Connect to MongoDB
mongo_uri = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(mongo_uri)

db = client["iot_environment"]
collection = db["sensor_readings"]

#Load data
data = list(collection.find())

temps = []
smokes = []
cos = []

for record in data:

    temp = record.get("temp")
    smoke = record.get("smoke")
    co = record.get("co")

    if temp is not None:
        temps.append(temp)

    if smoke is not None:
        smokes.append(smoke)

    if co is not None:
        cos.append(co)

#Thresholds
TEMP_HIGH = 30.4
TEMP_LOW = 11
SMOKE_HIGH = 0.042
CO_HIGH = 0.012

#Temperature plot
plt.figure(figsize=(8, 5))
plt.hist(temps, bins=30)
plt.axvline(
    TEMP_HIGH,
    linestyle="--",
    label="High threshold"
)
plt.axvline(
    TEMP_LOW,
    linestyle="--",
    label="Low threshold"
)
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.legend()
plt.savefig(
    "output/temp_distribution.png"
)
plt.close()

#Smoke plot
plt.figure(figsize=(8, 5))
plt.hist(smokes, bins=30)
plt.axvline(
    SMOKE_HIGH,
    linestyle="--",
    label="Threshold"
)
plt.title("Smoke Distribution")
plt.xlabel("Smoke")
plt.ylabel("Frequency")
plt.legend()
plt.savefig(
    "output/smoke_distribution.png"
)
plt.close()

#CO plot
plt.figure(figsize=(8, 5))
plt.hist(cos, bins=30)
plt.axvline(
    CO_HIGH,
    linestyle="--",
    label="Threshold"
)
plt.title("CO Distribution")
plt.xlabel("CO")
plt.ylabel("Frequency")
plt.legend()
plt.savefig(
    "output/co_distribution.png"
)
plt.close()

#Load outputs
with open(
    "output/municipal_report.json"
) as f:
    municipal_report = json.load(f)

with open(
    "output/system_health.json"
) as f:
    system_health = json.load(f)

with open(
    "output/batch_status.json"
) as f:
    batch_status = json.load(f)

with open(
    "output/warning_counts.json"
) as f:
    warning_counts = json.load(f)

with open(
    "output/alerts.json"
) as f:
    alerts = json.load(f)


#Top alert sensors
sensor_counter = Counter()

for alert in alerts:
    sensor_counter[
        alert["sensor"]
    ] += 1


top_sensors = sensor_counter.most_common(5)

#Sensor names for better readability
sensor_names = {
    "b8:27:eb:bf:9d:51": "Kungwini (Sensor 1)",
    "00:0f:00:70:91:0a": "Zithobeni (Sensor 2)",
    "1c:bf:ce:15:ec:4d": "Erasmus (Sensor 3)"
}

#Latest alert
if alerts:
    latest_alert = alerts[-1]

    latest_alert["sensor"] = sensor_names.get(
        latest_alert["sensor"],
        latest_alert["sensor"]
    )
else:
    latest_alert = {
        "sensor": "None",
        "type": "No alerts",
        "value": "-"
    }

top_sensor_html = ""

for sensor, count in top_sensors:

    display_name = sensor_names.get(sensor, sensor)

    top_sensor_html += (
        f"<li>{display_name}: "
        f"{count} alerts</li>"
    )

#Operational summary
if top_sensors:
    highest_sensor = top_sensors[0][0]
    highest_count = top_sensors[0][1]

    display_name = sensor_names.get(
        highest_sensor,
        highest_sensor
    )

    operational_message = (
        f"{display_name} generated "
        f"{highest_count} environmental alerts "
        "during the latest processing cycle. "
        "Consider dispatching an investigation "
        "or maintenance team."
    )
else:
    operational_message = (
        "No environmental alerts were detected "
        "during the latest processing cycle."
    )

#Health explanation
if system_health["pipeline_status"] == "healthy":
    health_message = (
        "All batches completed successfully. "
        "No loading problems were detected."
    )
else:
    health_message = (
        "Processing issues were detected. "
        "Review failed batches and invalid records."
    )

#Batch status - Rerun if failed
if batch_status["status"] == "completed":
    batch_message = (
        "All expected records were successfully processed."
    )
else:
    batch_message = (
    "Processing is incomplete. "
    "The number of processed records is lower than expected. "
    "Re-run the pipeline to process the remaining records."
    )


#Municipal dashboard
html = f"""
<html>
<head>
<title>Municipal Environmental Dashboard</title>
</head>

<body>

<h1>
Municipal Environmental Information Service
</h1>

<h2>Operational Summary</h2>

<p>
{operational_message}
</p>

<hr>

<h2>Planner Message</h2>

<p>
{municipal_report['planner_message']}
</p>

<h2>Recommended Action</h2>
<p>
{municipal_report['recommended_action']}
</p>

<h2>Data Quality</h2>

<p>
{municipal_report['data_quality_message']}
</p>

<h2>Service Status</h2>
<p>
{municipal_report['service_status']}
</p>

<hr>

<h2>Latest Alert</h2>

<p>
<b>Sensor:</b>
{latest_alert['sensor']}<br>

<b>Type:</b>
{latest_alert['type']}<br>

<b>Value:</b>
{latest_alert['value']}
</p>

<hr>

<h2>Environmental Alert Summary</h2>

<ul>
<li>
High Temperature Threshold Exceeded:
{warning_counts['high_temp']}
</li>

<li>
Low Temperature Threshold Exceeded:
{warning_counts['low_temp']}
</li>

<li>
Smoke Threshold Exceeded:
{warning_counts['high_smoke']}
</li>

<li>
Carbon Monoxide Threshold Exceeded:
{warning_counts['high_co']}
</li>
</ul>

<hr>

<h2>Top Alert Sensors</h2>

<p>
Sensors generating the highest number of alerts
may require investigation.
</p>

<ul>
{top_sensor_html}
</ul>

<hr>

<h2>Data Input Health</h2>

<p>
{health_message}
</p>

<p>
Checks loading success, invalid records and
overall processing health.
</p>

<ul>
<li>
Pipeline status:
{system_health['pipeline_status']}
</li>

<li>
MongoDB connection:
{system_health['mongodb_connection']}
</li>

<li>
Failed batches:
{system_health['failed_batches']}
</li>

<li>
Invalid records:
{system_health['invalid_records']}
</li>

<li>
Last successful run:
{system_health['last_successful_run']}
</li>
</ul>

<hr>

<h2>Batch Processing Status</h2>

<p>
{batch_message}
</p>

<ul>

<li>
Last completed batch:
{batch_status['last_batch']}
</li>

<li>
Expected records:
{batch_status['expected_records']}
</li>

<li>
Records loaded:
{batch_status['records_loaded']}
</li>

<li>
Failed batches:
{batch_status['failed_batches']}
</li>

<li>
Status:
{batch_status['status']}
</li>

</ul>

<hr>

<h2>Supporting Visualisations</h2>

<p>
Distribution plots support interpretation
of environmental conditions.
</p>

<img src="temp_distribution.png"
width="600"><br><br>

<img src="smoke_distribution.png"
width="600"><br><br>

<img src="co_distribution.png"
width="600"><br><br>

</body>
</html>
"""

with open(
    "output/municipal_dashboard.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(html)

print(
    "Visualisations and dashboard created."
)
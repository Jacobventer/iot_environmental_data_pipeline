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

#Municipal dashboard
html = f"""
<html>
<head>
<title>Municipal Environmental Dashboard</title>
</head>

<body>

<h1>Municipal Environmental Information Service</h1>

<h2>Planner Message</h2>
<p>{municipal_report['planner_message']}</p>

<h2>Recommended Action</h2>
<p>{municipal_report['recommended_action']}</p>

<h2>Service Status</h2>
<p>{municipal_report['service_status']}</p>

<h2>System Health</h2>
<pre>{json.dumps(system_health, indent=4)}</pre>

<h2>Batch Status</h2>
<pre>{json.dumps(batch_status, indent=4)}</pre>

<h2>Warning Counts</h2>
<pre>{json.dumps(warning_counts, indent=4)}</pre>

<h2>Visualisations</h2>

<img src="temp_distribution.png" width="600"><br><br>
<img src="smoke_distribution.png" width="600"><br><br>
<img src="co_distribution.png" width="600"><br><br>

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
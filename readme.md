# IoT Environmental Data Pipeline
## Overview
This project implements a portable environmental monitoring pipeline for a municipal information service.  

Environmental sensor telemetry data is loaded into MongoDB in batches, analysed for abnormal conditions and   
transformed into environmental alerts, monitoring outputs and a planner-facing dashboard.  
The system generates environmental alerts, monitoring information and a dashboard to help Kungwini municipal city planners.  

This project was developed as part of a Data Engineering portfolio assignment.  

________________________________________

## Operational Scenario
Environmental sensors are deployed throughout the Kungwini municipality and collect measurements at regular intervals.  

The municipal environmental team runs the pipeline every 6 hours to load newly collected telemetry data into the system.  
During each execution, the new sensor data is processed in batches of 10,000 records to reduce memory usage, improve performance   
and maintain processing stability when handling large datasets. Processing continues until all records have been loaded.   
The dashboard is then updated with the latest environmental alerts, monitoring information and health indicators.   
If processing is incomplete, the dashboard reports the number of expected and processed records and recommends re-running the pipeline.

The generated dashboard allows city planners to:

- Monitor environmental conditions
- Review environmental alerts
- Identify sensors requiring investigation
- Monitor data quality
- Monitor processing health
- Dispatch maintenance or investigation teams when required

This system is intended as an environmental information service and not as a real-time emergency response system.

________________________________________

## Repository Structure

iot_environmental_data_pipeline/  
│
├── data/  
│   └── iot_telemetry_data.csv  
│  
├── scripts/  
│   ├── init_db.py  
│   ├── load_data.py  
│   ├── analyze_data.py  
│   └── visualize.py  
│  
├── output/  
├── logs/  
│  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
└── README.md  


________________________________________

## Architecture 

CSV Dataset  
       ↓  
Chunk Loading (10,000 records)  
       ↓  
MongoDB  
       ↓  
Analysis & Alert Generation  
       ↓  
Monitoring & Health Checks  
       ↓  
Municipal Dashboard  
       ↓  
Planner Review  

________________________________________

## Components  

### init_db.py  
•	Creates the MongoDB database  
•	Creates the sensor collection  
•	Creates indexes  

### load_data.py
•	Loads the dataset using chunk processing  
•	Batch size: 10,000 records  
•	Tracks loading status  
•	Tracks invalid records  
•      Detects incomplete processing  
•	Generates system-health outputs  

### analyze_data.py  
•	Processes environmental telemetry   
•	Generates environmental alerts    
•	Calculates alert counts and summary statistics   
•      Creates planner-facing messages and recommended actions
•      Tracks data quality, invalid records, processing health and the time of the last successful data load


### visualize.py  
•	Creates environmental visualisations  
•	Generates the municipal dashboard  
•      Displays planner recommendations
•      Displays environmental alert locations
•      Displays data-quality and system-health information
•      Displays batch-processing status and incomplete-processing warnings
       
________________________________________

## Dashboard Features  
The dashboard provides:  

•	Planner messages  
•	Recommended actions  
•	Data-quality information  
•	Latest environmental alert  
•      Environmental alert counts
•      Alert locations 
•      Operational summary
•      Data-quality and processing health
•      Last successful data load
•      Batch-processing status  

________________________________________

## Outputs  

### Operational Outputs  
•	alerts.json  
•	warning_counts.json  
•	summary.json  
•	municipal_report.json  

### Monitoring Outputs  
•	batch_status.json  
•	system_health.json  
•	pipeline.log  

### Dashboard Outputs  
•	municipal_dashboard.html  
•	temp_distribution.png  
•	smoke_distribution.png  
•	co_distribution.png  

________________________________________

## Technology Stack  
•	Python  
•	MongoDB  
•	Docker  
•	Docker Compose  
•	Pandas  
•	Matplotlib  

________________________________________

## Running the Project

### 1. Clone the Repository  

```
git clone https://github.com/Jacobventer/iot_environmental_data_pipeline.git  

cd iot_environmental_data_pipeline
```

### 2. Download the Dataset    

Download:  
iot_telemetry_data.csv  
from: 
[Data set](https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input  )

Place the file in:  
data/  

### 3. Run the Pipeline  
```
docker compose up --build
```
The pipeline will: 

•	Initialise MongoDB  
•	Load telemetry data  
•	Generate alerts  
•	Perform monitoring checks  
•	Create dashboard outputs  

### 4. View the Dashboard  

Open:  
output/municipal_dashboard.html  

________________________________________


 
## Author  

Jaco Venter  
BSc Data Science  
[LinkedIn Profile](https://www.linkedin.com/in/jaco-venter-45502a162/) 

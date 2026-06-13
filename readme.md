# IoT Environmental Data Pipeline
## Overview
This project implements a portable environmental monitoring pipeline for a municipal information service.  
Environmental sensor telemetry is loaded into MongoDB, analysed for abnormal conditions and transformed into planner-facing outputs. The system generates environmental alerts, monitoring information and a dashboard to support municipal decision-making.  
This project was developed as part of a Data Engineering portfolio assignment.  
________________________________________
## Operational Scenario
Environmental sensors are deployed throughout the Kungwini municipality and collect measurements at regular intervals.  
Telemetry data is processed every 6 hours in batches. The generated dashboard allows city planners to:  
•	Monitor environmental conditions  
•	Review environmental alerts  
•	Identify sensors requiring investigation  
•	Monitor data quality  
•	Monitor processing health  
•	Dispatch maintenance or investigation teams when required  
This system is intended as an environmental information service and not as a real-time emergency response system.  
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
•	Generates system-health outputs  
### analyze_data.py  
•	Processes environmental telemetry  
•	Generates alerts  
•	Calculates warning counts  
•	Creates planner-facing recommendations  
•	Generates monitoring outputs  
### visualize.py  
•	Creates environmental visualisations  
•	Generates the municipal dashboard  
•	Displays alerts, health information and batch status  
________________________________________
## Dashboard Features  
The dashboard provides:  
•	Planner messages  
•	Recommended actions  
•	Data-quality information  
•	Latest environmental alert  
•	Alert counts  
•	Top warning sensors  
•	Data-input health  
•	Batch-processing status  
•	Environmental visualisations  
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
https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input  
Place the file in:  
data/  
### 3. Run the Pipeline  
docker compose up –build  
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
 
## Author  
Jaco Venter  
BSc Data Science  
International University of Applied Sciences (IU)  


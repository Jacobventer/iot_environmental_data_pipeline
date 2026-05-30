# IoT Environmental Sensor Data Pipeline
## Overview

The aim of this project was to design and implement a portable data engineering system for municipal environmental monitoring.

Environmental sensor deployments generate large volumes of telemetry data. Municipal planners require reliable environmental information to support long-term planning and environmental risk identification. This project implements a Dockerized batch-processing pipeline that loads, analyses and visualises environmental sensor telemetry data.

The system is designed as an information service rather than a real-time critical alert system. Its purpose is to support decision-making through environmental monitoring, alerts, system-health reporting and planner-facing outputs.

## Problem Statement

Municipal planners require quality environmental information to improve long-term city conditions and support future environmental warning systems.  

Future sensor structures are unknown. Therefore, the database must support schema flexibility and easy expansion without requiring major restructuring.  

## The system should:  

- Store large volumes of sensor data efficiently
- Handle evolving sensor structures
- Provide meaningful insights and environmental alerts
- Monitor pipeline and data-input health
- Support future front-end integration and dashboards

  
This project simulates a backend environmental information system for municipal use.  

## Context of Use  

This project models a municipal environmental information service.  

Environmental telemetry is processed in recurring batches and analysed to identify abnormal conditions such as high temperature, smoke or carbon monoxide levels.

City planners review the generated dashboard and reports to:

- Monitor environmental conditions
- Identify areas requiring investigation
- Send out mainanace teams
- Review warning patterns
- Monitor data quality and pipeline health

The system does not guarantee real-time accuracy. Missing or delayed data may reduce confidence, but such limitations are acceptable for an information service designed to support decision-making.

  
## Project Structure
iot-environmental-sensor-data-pipeline/  
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
│   ├── alerts.json  
│   ├── warning_counts.json  
│   ├── summary.json  
│   ├── batch_status.json  
│   ├── system_health.json  
│   ├── municipal_report.json  
│   ├── municipal_dashboard.html  
│   ├── temp_distribution.png  
│   ├── smoke_distribution.png  
│   └── co_distribution.png  
│  
├── logs/  
│   └── pipeline.log  
│  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
└── README.md    
  
## Dataset

This project uses the Environmental Sensor Telemetry Dataset from Kaggle.

Dataset size:

405,184 rows
9 columns

Available at:

https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input

The dataset includes:

Temperature
Humidity
Carbon monoxide
Light intensity
Smoke levels
Time-stamped telemetry readings

The dataset closely matches the environmental monitoring use case of this project.

## Technology Stack
- MongoDB – Schema-flexible document database
- Docker & Docker Compose – Portable deployment and orchestration
- Python – Data loading and analysis
- Pandas – Batch and chunk processing
- Matplotlib – Visualisation
- GitHub – Version control and documentation

## System Architecture

Environmental telemetry is processed using a sequential data pipeline:

CSV → Chunk Loading → MongoDB → Analysis → Monitoring → Dashboard → Planner Review

### Components   
1. Database Initialisation (init_db.py)
- Creates MongoDB database and collection
- Creates indexes for improved access  
  
2. Data Loading (load_data.py)
- Loads CSV using chunk loading
- Processes data in batches of 10 000 records
- Validates missing values
- Skips invalid records
- Implements retry logic for MongoDB failures
- Creates loading and health outputs  

3. Analysis (analyze_data.py)
- Processes MongoDB data sequentially
- Applies environmental thresholds
- Generates alerts
- Computes summary statistics
- Produces planner-facing municipal reports  
  
4. Visualisation (visualize.py)

Creates a municipal dashboard containing:

- Planner message
- Recommended action
- Latest alert
- Alert counts
- Top alert sensors
- Data-input health
- Batch-processing status
- Supporting visualisations  
  
5. Monitoring and Logging

Pipeline health monitoring includes:

- Batch tracking
- Invalid record monitoring
- MongoDB connection monitoring
- Logging via pipeline.log

## Environmental Alerts

Thresholds are used to detect abnormal environmental conditions.

Temperature
- High > 30.4°C
- Low < 11°C
- Smoke
- High > 0.042
- Carbon Monoxide
- High > 0.012

## Outputs

The pipeline produces the following outputs.

### Operational Outputs
- alerts.json – Individual environmental alerts
- warning_counts.json – Alert frequency summary
- summary.json – Statistical summaries
- municipal_report.json – Planner-facing information service output  

### Monitoring Outputs
- batch_status.json – Batch progress and loading status
- system_health.json – Pipeline and data-input health
- logs/pipeline.log – System activity and troubleshooting  

### Dashboard and Visualisations
- municipal_dashboard.html – Planner dashboard
- temp_distribution.png
- smoke_distribution.png
- co_distribution.png


## How to Run
### Prerequisites
Docker Desktop installed and running

### Steps
### 1. Clone the Repository
```
git clone https://github.com/Jacobventer/iot_environmental_data_pipeline.git
cd iot_environmental_data_pipeline
```
### 2. Download Dataset 

Download:
```
iot_telemetry_data.csv
```
from:  
https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input

Place the file inside:  
data/  

### 3. Run the Pipeline
docker compose up --build

This will:

Start MongoDB
Initialise the database
Load data using chunk processing
Analyse environmental conditions
Generate monitoring outputs
Create the municipal dashboard
### 4. View Outputs

Generated in:  
  
output/  
logs/  

Open:  
```  
output/municipal_dashboard.html  
```
to view the planner dashboard.

## Troubleshooting
|     Problem       |	   Solution                      |  
|------|------|
|Docker not running	| Start Docker Desktop             |  
|Connection refused |	Wait for MongoDB startup         |  
|File not found     | Verify CSV location and filename |  
|Port 27017 in use	| Stop local MongoDB instance      |  

## Notes

This project was developed as part of a Data Engineering portfolio assignment.

The project focuses on portable backend environmental monitoring and municipal information services.

The system is designed to support decision-making and does not represent a real-time critical infrastructure system.

## Author
Jaco Venter  
BSc Data Science  
International University of Applied Science (Germany)  

LinkedIn:  
https://www.linkedin.com/in/jaco-venter-45502a162/  

## License  
This project is licensed under the MIT License.

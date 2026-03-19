# IoT Environmental Sensor Data Pipeline
## Overview

The aim of this project was to design and implement a portable data engineering system.  
The pipeline loads, stores, and analyses environmental telemetry data to support municipal decision making and alert system.

Environmental sensor deployments generate large volumes of time-series data.  
To support future scalability and long-term planning, this project provides a Dockerized batch-processing pipeline.  


## Problem Statement

Municipal planners need quality historical environmental data. This can help improve long term city condictions and help with a citizen alterting applicaiton.
Future sensor structures are unknown so the database must be able to handle a flexible schema and allow easy extension without restructuring the entire system.   

The system should:
- Store large volumes of sensor data efficiently  
- Handle evolving sensor structures (schema flexibility)  
- Provide meaningful insights (alerts and summaries)  
- Support integration with future front-end applications

This project simulates a backend system that enables environmental monitoring and alert generation.


## Project Structure
```bash
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

```

## Dataset

The dataset used in this project is the *Environmental Sensor Telemetry Dataset* from Kaggle (405,184 rows × 9 columns).    

Available at: [Data set](https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input)

Each record is time-stamped and includes measurements such as:
- Temperature  
- Humidity  
- Carbon monoxide  
- Light intensity  
- Smoke levels

With 405,184 entries the dataset closely matches the project’s requirements and use case of environmental IoT telemetry data.

## Technology Stack

- **MongoDB** – Document-oriented database for schema-flexible storage  
- **Docker & Docker Compose** – Containerization and environment management  
- **Python** – Batch loading
- **Matplotlib** – Data visualization
- **GitHub** – Version control and documentation

## System Architecture

CSV → Data Loading → MongoDB → Analysis → Visualization → Outputs

Components:
1. **Data loader** (load_data.py)
   - Loads CSV data into MongoDB in batches
   - Includes retry logic for database connection
   - Logs pipeline execution
2. **Data Analysis** (analyze_data.py)
   - Applies environmental thresholds
   - Generates alerts for abnormal conditions
   - Computes summary statistics
   - Counts warning events
3. **Visualisation** (visualize.py)
   - Generates distribution plots for each metric
   - Highlights threshold levels
4. **Logging & Monitoring**
   - Logs pipeline activity in logs/pipeline.log
   - Provides basic health monitoring and error tracking

## Alerts

Thresholds are used to detect abnormal conditions:
1. Temperature:
   - High > 30.4°C
   - Low < 11°C
2.	Smoke:
   - High > 0.042
3. CO:
   -High > 0.012

## Outputs

1. Alerts - output/alerts.json
2. Warning counts - output/warning_counts.json
3. Summary statistics - output/summary.json
4. Visualization - output/temp_distribution.png, output/smoke_distribution.png, output/co_distribution.png
5. Logs - logs/pipeline.log


## How to Run
### Prerequisites
- Docker Desktop installed and running

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Jacobventer/iot_environmental_data_pipeline.git
   cd iot_environmental_data_pipeline
   ```
   
2. Download the dataset  
   Go to: [data set](https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input)
   Download iot_telemetry_data.csv  
   Place the file in the data/folder
   
3. Run the pipline
   ```bash
   docker compose up --build
   ```
   This will:
   - Start MongoDB
   - Initialize the dataset
   - Load all 405 184 records in batches
   - Print total record count
    
4. Outputs will be generated in:
   outputs/
   logs/
   
## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not running |Start Docker Desktop |
| Connection refused | Wait 10 seconds for MongoDB to fully start |
| File not found | Ensure CSV is in `data/` folder with correct name |
| Port 27017 already in use | Stop any local MongoDB: `sudo service mongod stop` |


## Notes
This project was developed as part of a Data Engineering portfolio assignment.      
This project focuses on building a backend data system.   
The system is designed as an information service to support decision-making rather than a real-time critical alert system.  
The outputs are designed to be integrated into future front-end applications such as dashboards or citizen alert application.  



## Author
Jaco Venter

BSc Data Science 
International University of Applied Science (Germany)

[LinkedIn Profile](https://www.linkedin.com/in/jaco-venter-45502a162/)

## License
This project is licensed under the MIT License.

# IoT Environmental Sensor Data Pipeline
## Overview

The aim of this project was to build and implement a portable data engineering system.  
The pipeline should be able to load, store, and manage IoT environmental sensor telemetry data for municipal analysis of a smart city.

Environmental sensor deployments produce large volumes of time-series data. 
To suppurt future scalability and long term planning, this project provides a Dockerised pipeline.  
Environmental IoT device data in loaded into a schema-flexible dattabase, MongoDB.   
This will help with future sensor integration of known structured data.  



## Problem Statement

Municipal planners need quality historical environmental data. This can help improve long term city condictions and help with a citizen alterting applicaiton.
Future sensor structures are unknown so the database must be able to handle a flexible schema.

## Project Structure
```bash
iot-environmental-sensor-data-pipeline/
│
├── data/
│   └── iot_telemetry_data.csv
│
├── scripts/
│   ├── init_db.py
│   └── load_data.py
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

Wtth 405,184 entries the dataset closely matches the project’s requirements and use case of environmental IoT telemetry data.

## Technology Stack

- **MongoDB** – Document-oriented database for schema-flexible storage  
- **Docker & Docker Compose** – Containerization and environment management  
- **Python** – Batch loading
- **Jupyter Notebook** – Script development and testing  
- **GitHub** – Version control and documentation

## System Architecture

The pipeline consists of:

1. **Dockerized MongoDB instance**  
2. **Database initialization script** (`init_db.py`)  
3. **Data loading script** (`load_data.py`)  
4. **Batch loading**  
5. **Automated startup via `docker compose up`**
6. **Data verification**

## How to Run
### Prerequisites
- Docker Desktop installed and running

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/iot-environmental-sensor-data-pipeline.git
   cd iot-environmental-sensor-data-pipeline
   ```
2. Download the dataset
   Go to: [data set](https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input)
   Download iot_telemetry_data.csv
   Place the file in the data/ folder
3. Run the pipline
   ```bash
   docker compose up --build
   ```
   This will:
   - Start MongoDB
   - Initialize the dataset
   - Load all 405 184 records in batches
   - Print total record count
    
4. Verify the data loaded
   Open a new terminal and run:
   ```bash
   docker exec -it mongodb mongosh
   ```
   Then inside MongoDB, run:
   ```bashjavascript
   use iot_environment
   db.sensor_readings.countDocuments()
   ```
   Expected result:
   ```code
   405184
   ```
   
## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not running |Start Docker Desktop |
| Connection refused | Wait 10 seconds for MongoDB to fully start |
| File not found | Ensure CSV is in `data/` folder with correct name |
| Port 27017 already in use | Stop any local MongoDB: `sudo service mongod stop` |


## Notes
This project was developed as part of a Data Engineering portfolio assignment.  
The focus is on portability, scalability, and maintainability rather than real-time streaming or front-end visualization.

## Author
Jaco Venter

BSc Data Science student at International University of Applied Science (Germany)

[LinkedIn Profile](https://www.linkedin.com/in/jaco-venter-45502a162/)

## License
This project is licensed under the MIT License.

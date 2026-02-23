# IoT Environmental Sensor Data Pipeline
## Overview

This project implements a portable data engineering system to ingest, store, and manage IoT environmental sensor telemetry data for municipal analysis and citizen alerting. 
The focus is on modern data engineering practices such as containerization, batch ingestion, and scalable storage.

Environmental sensor deployments produce large volumes of time-series data. To support long-term planning and analytical needs, this project implements a **Dockerized pipeline** that loads environmental sensor data into a **schema-flexible database (MongoDB)** in batches, ensuring future adaptability when new sensors with unknown structures are introduced.

## Problem Statement

Municipal planners require reliable historical insights into environmental conditions, and real-time data availability to alert citizens when thresholds are exceeded. 
However, sensor structures may vary and evolve in the future, making fixed database schemas impractical. This system addresses schema flexibility, portability, and maintainability.

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
Availible at: https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input

Each record is time-stamped and includes measurements such as:
- Temperature  
- Humidity  
- Carbon monoxide  
- Light intensity  
- Smoke levels

This dataset closely matches the project’s use case of environmental IoT telemetry.

## Technology Stack

- **MongoDB** – Document-oriented database for schema-flexible storage  
- **Docker & Docker Compose** – Containerization and environment management  
- **Python** – Batch data ingestion and database interaction 
- **Jupyter Notebook** – Script development and testing  
- **GitHub** – Version control and documentation

## System Architecture

The system consists of:

1. **Dockerized MongoDB instance**  
2. **Database initialization script** (`init_db.py`)  
3. **Data ingestion script** (`load_data.py`)  
4. **Batch loading from CSV file**  
5. **Automated startup via `docker compose up`**

## How to Run

### Prerequisites
- Docker
- Docker Compose

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/iot-environmental-sensor-data-pipeline.git
2. Navigate to the project directory:
```
cd Documents
```
3. Start the data pipeline using Docker Compose:
``` bash
cd iot-environmental-sensor-data-pipeline
```
This command starts a MongoDB container and automatically executes the Python scripts to initialize the database and load the environmental sensor data in batches.
To stop the system, press CTRL + C, and optionally remove the containers with:
``` bash
docker compose down
```

## Notes
This project was developed as part of a Data Engineering portfolio assignment. The focus is on portability, scalability, and maintainability rather than real-time streaming or front-end visualization.

## Author
Jaco Venter

BSc Data Science student at International University of Applied Scinece (Germany)

https://www.linkedin.com/in/jaco-venter-45502a162/

## License
This project is licensed under the MIT License.

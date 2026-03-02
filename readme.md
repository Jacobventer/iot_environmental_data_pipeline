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
Available at: [Data set](https://www.kaggle.com/code/rjconstable/environmental-sensor-telemetry-dataset/input)

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
   Start MongoDB
   Load all 405,184 sensor records automatically
4. Verify the data loaded
   Open a new terminal and run:
   ```bash
   docker exec -it iot-environmental-sensor-data-pipeline-mongodb-1 mongosh
   ```
   Then inside MongoDB, run:
   ```bashjavascript
   show dbs
   use sensor_db
   db.sensor_readings.countDocuments()
   ```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Wait 10 seconds for MongoDB to fully start |
| File not found | Ensure CSV is in `data/` folder with correct name |
| Port 27017 already in use | Stop any local MongoDB: `sudo service mongod stop` |
| Permission denied | On Linux, you may need `sudo` for docker commands |

## Docker Configuration
- Dockerfile
- docker-compose.yml - Orchestrates MongoDB + Python loader
- Volumes - Persists MongoDB data between restarts

## Notes
This project was developed as part of a Data Engineering portfolio assignment. The focus is on portability, scalability, and maintainability rather than real-time streaming or front-end visualization.

## Author
Jaco Venter

BSc Data Science student at International University of Applied Science (Germany)

[LinkedIn Profile](https://www.linkedin.com/in/jaco-venter-45502a162/)

## License
This project is licensed under the MIT License.

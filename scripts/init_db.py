from pymongo import MongoClient
import os

#Connect to MongoDB 
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

#Create database
db = client["iot_environment"]

#Create collection
collection = db["sensor_readings"]

print("MongoDB connection successful.")
print("Database and collection initialized.")

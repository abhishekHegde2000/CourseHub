import json
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, CollectionInvalid
import os

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

# Function to check if MongoDB is connected


def check_db_connection(client):
    try:
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        print("MongoDB connection: Successful")
    except ConnectionFailure:
        print("MongoDB connection: Failed")
        raise

# Function to populate MongoDB with data from courses.json


def populate_db():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        check_db_connection(client)

        db = client[MONGO_DB]

        # Check if the collection exists, if not create it
        if 'courses' not in db.list_collection_names():
            try:
                courses_collection = db.create_collection('courses')
                print("Collection 'courses' created.")
            except CollectionInvalid:
                courses_collection = db.courses
                print("Collection 'courses' already exists.")
        else:
            courses_collection = db.courses

        # Read courses.json
        with open('courses.json', 'r') as file:
            courses = json.load(file)

        # Insert data into MongoDB
        courses_collection.insert_many(courses)

        # Create indices for efficient retrieval
        courses_collection.create_index([("name", ASCENDING)])
        courses_collection.create_index([("date", DESCENDING)])
        courses_collection.create_index([("domain", ASCENDING)])

        print("Data populated and indices created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    populate_db()

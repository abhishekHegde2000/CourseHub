import json
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, CollectionInvalid, PyMongoError

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")


def check_db_connection(client):
    """Checks if MongoDB is connected."""
    try:
        client.admin.command('ping')
        print("MongoDB connection: Successful")
    except ConnectionFailure:
        print("MongoDB connection: Failed")
        raise


def populate_db():
    """Populates MongoDB with data from courses.json."""
    try:
        client = MongoClient(MONGO_URL)
        check_db_connection(client)
        db = client[MONGO_DB]

        if 'courses' not in db.list_collection_names():
            try:
                courses_collection = db.create_collection('courses')
                print("Collection 'courses' created.")
            except CollectionInvalid:
                courses_collection = db.courses
                print("Collection 'courses' already exists.")
        else:
            courses_collection = db.courses

        with open('courses.json', 'r') as file:
            courses = json.load(file)

        courses_collection.insert_many(courses)
        courses_collection.create_index([("name", ASCENDING)])
        courses_collection.create_index([("date", DESCENDING)])
        courses_collection.create_index([("domain", ASCENDING)])

        print("Data populated and indices created successfully.")
    except (ConnectionFailure, CollectionInvalid, PyMongoError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    try:
        populate_db()
    except Exception as e:
        print(f"Failed to populate the database: {e}")

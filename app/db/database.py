import json
import os
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, CollectionInvalid, PyMongoError
from pymongo.collection import Collection

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")


def get_client() -> MongoClient:
    """Create and return a MongoClient instance."""
    client = MongoClient(MONGO_URL)
    try:
        client.admin.command('ping')
        print("MongoDB connection: Successful")
    except ConnectionFailure:
        print("MongoDB connection: Failed")
        raise
    return client


def get_db() -> MongoClient:
    """Get the database instance."""
    client = get_client()
    return client[MONGO_DB]


def get_courses_collection() -> Collection:
    """Get the courses collection."""
    db = get_db()
    try:
        if 'courses' not in db.list_collection_names():
            courses_collection = db.create_collection('courses')
            print("Collection 'courses' created.")
        else:
            courses_collection = db.courses
            print("Collection 'courses' already exists.")
    except CollectionInvalid:
        courses_collection = db.courses
        print("Collection 'courses' already exists.")

    return courses_collection


def populate_db():
    """Populates MongoDB with data from courses.json."""
    courses_collection = get_courses_collection()
    try:
        # Delete all documents in the collection
        courses_collection.delete_many({})
        print("All documents in the 'courses' collection have been deleted.")

        with open('courses.json', 'r') as file:
            courses = json.load(file)

        # Ensure each chapter has a unique ID
        for course in courses:
            for chapter in course.get("chapters", []):
                if "id" not in chapter:
                    chapter["id"] = str(ObjectId())

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

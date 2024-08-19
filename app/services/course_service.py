from typing import List, Optional
from app.models.course_model import Course, Chapter
from pymongo import MongoClient, ASCENDING, DESCENDING
from fastapi import HTTPException
import os

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
courses_collection = db.courses


def get_all_courses(sort_by: str, domain: Optional[str]):
    query = {}
    if domain:
        query["domain"] = domain

    sort_field = {
        "alphabetical": ("name", ASCENDING),
        "date": ("date", DESCENDING),
        "rating": ("total_rating", DESCENDING)
    }.get(sort_by, ("name", ASCENDING))

    courses = list(courses_collection.find(query).sort([sort_field]))
    return [Course(**course) for course in courses]


def get_course_overview(course_id: str):
    course = courses_collection.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return Course(**course)


def get_chapter_info(course_id: str, chapter_id: str):
    course = courses_collection.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = next(
        (ch for ch in course["chapters"] if ch["id"] == chapter_id), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return Chapter(**chapter)


def rate_chapter(course_id: str, chapter_id: str, rating: int):
    course = courses_collection.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = next(
        (ch for ch in course["chapters"] if ch["id"] == chapter_id), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    chapter["total_rating"] += rating
    courses_collection.update_one(
        {"_id": course_id}, {"$set": {"chapters": course["chapters"]}})
    return {"message": "Rating updated successfully"}

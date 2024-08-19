from bson import ObjectId
from fastapi import HTTPException
from pymongo import ASCENDING, DESCENDING
from typing import List, Optional, Dict, Any
from app.models.course_model import Course, Chapter
from pymongo.collection import Collection
from app.db.database import get_courses_collection
from app.services.transformation import transform_course, transform_chapter


def get_all_courses(sort_by: str, domain: Optional[str]) -> List[Course]:
    courses_collection = get_courses_collection()
    query = {}
    if domain:
        query["domain"] = domain

    sort_field = {
        "alphabetical": ("name", ASCENDING),
        "date": ("date", DESCENDING),
        "rating": ("total_rating", DESCENDING)
    }.get(sort_by, ("name", ASCENDING))

    courses = list(courses_collection.find(query).sort([sort_field]))
    return [transform_course(course) for course in courses]


def get_course_overview(course_id: str) -> Course:
    courses_collection = get_courses_collection()
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return transform_course(course)


def get_chapter_info(course_id: str, chapter_id: str) -> Chapter:
    courses_collection = get_courses_collection()
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = next((ch for ch in course.get("chapters", [])
                   if str(ch.get("id")) == chapter_id), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return transform_chapter(chapter)


def rate_chapter(course_id: str, chapter_id: str, rating: int) -> Dict[str, Any]:
    courses_collection = get_courses_collection()
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = next((ch for ch in course.get("chapters", [])
                   if str(ch.get("id")) == chapter_id), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    new_rating = chapter.get("total_rating", 0) + rating
    courses_collection.update_one(
        {"_id": ObjectId(course_id), "chapters.id": chapter_id},
        {"$set": {"chapters.$.total_rating": new_rating}}
    )
    return {"message": "Rating updated successfully", "rating": new_rating}

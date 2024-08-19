from typing import Dict, Any
from bson import ObjectId
from app.models.course_model import Course, Chapter


def transform_course(course_doc: Dict[str, Any]) -> Course:
    return Course(
        id=str(course_doc["_id"]),
        name=course_doc["name"],
        date=course_doc["date"],
        description=course_doc["description"],
        domain=course_doc["domain"],
        chapters=[
            Chapter(
                # Generate a default ID if not present
                id=str(chapter.get("id", ObjectId())),
                name=chapter["name"],
                text=chapter["text"]
            )
            for chapter in course_doc.get("chapters", [])
        ],
        total_rating=course_doc.get("total_rating", 0)
    )


def transform_chapter(chapter_doc: Dict[str, Any]) -> Chapter:
    return Chapter(
        # Generate a default ID if not present
        id=str(chapter_doc.get("_id", ObjectId())),
        name=chapter_doc["name"],
        text=chapter_doc["text"]
    )

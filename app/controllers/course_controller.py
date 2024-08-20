from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import ValidationError
from app.models.course_model import Course
from app.schemas.schema import ChapterSchema, CourseSchema, RateResponseSchema
from app.services.course_service import (
    get_all_courses,
    get_course_overview,
    get_chapter_info,
    rate_chapter
)
from app.middlewares.logging import logger

router = APIRouter()


@router.get("/courses", response_model=List[CourseSchema])
def list_courses(
    sort_by: Optional[str] = Query(
        "alphabetical", description="Sort by: 'alphabetical', 'date', or 'rating'"),
    domain: Optional[str] = Query(None, description="Filter courses by domain")
):
    try:
        courses = get_all_courses(sort_by, domain)
        logger.info("Fetched courses list successfully.")
        return courses
    except ValidationError as e:
        logger.error(f"Data validation error: {e.errors()}")
        logger.error(f"Offending data: {e.raw_data}")
        raise HTTPException(status_code=422, detail="Data validation error")
    except Exception as e:
        logger.error(f"Failed to list courses: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/courses/{course_id}", response_model=CourseSchema)
def course_overview(course_id: str):
    try:
        return get_course_overview(course_id)
    except HTTPException as e:
        logger.error(f"Course not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to get course overview: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/courses/{course_id}/chapters/{chapter_id}", response_model=ChapterSchema)
def chapter_info(course_id: str, chapter_id: str):
    try:
        return get_chapter_info(course_id, chapter_id)
    except HTTPException as e:
        logger.error(f"Chapter not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to get chapter info: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/courses/{course_id}/chapters/{chapter_id}/rate", response_model=RateResponseSchema)
def rate_chapter_endpoint(course_id: str, chapter_id: str, rating: int):
    try:
        rate_chapter(course_id, chapter_id, rating)
        return RateResponseSchema(message="Rating updated successfully")
    except HTTPException as e:
        logger.error(f"Failed to rate chapter: {e}")
        raise e
    except Exception as e:
        logger.error(f"Failed to rate chapter: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from fastapi import HTTPException
from app.services.course_service import rate_chapter

# Mock data
mock_course_id = str(ObjectId())
mock_chapter_id = "1"
mock_course = {
    "_id": ObjectId(mock_course_id),
    "chapters": [
        {"id": mock_chapter_id, "total_rating": 5}
    ]
}


@patch('app.services.course_service.get_courses_collection')
def test_rate_chapter_course_not_found(mock_get_courses_collection):
    # Mock the collection to return None for find_one
    mock_collection = MagicMock()
    mock_collection.find_one.return_value = None
    mock_get_courses_collection.return_value = mock_collection

    with pytest.raises(HTTPException) as exc_info:
        rate_chapter(mock_course_id, mock_chapter_id, 3)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Course not found"


@patch('app.services.course_service.get_courses_collection')
def test_rate_chapter_chapter_not_found(mock_get_courses_collection):
    # Mock the collection to return a course without the chapter
    mock_collection = MagicMock()
    mock_collection.find_one.return_value = {
        "_id": ObjectId(mock_course_id), "chapters": []}
    mock_get_courses_collection.return_value = mock_collection

    with pytest.raises(HTTPException) as exc_info:
        rate_chapter(mock_course_id, mock_chapter_id, 3)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Chapter not found"


@patch('app.services.course_service.get_courses_collection')
def test_rate_chapter_success(mock_get_courses_collection):
    # Mock the collection to return the course and update the rating
    mock_collection = MagicMock()
    mock_collection.find_one.return_value = mock_course
    mock_get_courses_collection.return_value = mock_collection

    response = rate_chapter(mock_course_id, mock_chapter_id, 3)

    assert response["message"] == "Rating updated successfully"
    assert response["rating"] == 8
    mock_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(mock_course_id), "chapters.id": mock_chapter_id},
        {"$set": {"chapters.$.total_rating": 8}}
    )

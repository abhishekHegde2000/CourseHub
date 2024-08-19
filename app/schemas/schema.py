from pydantic import BaseModel, Field
from typing import List

# MongoDB Chapter schema uses 'text' field instead of 'content'


class ChapterSchema(BaseModel):
    name: str = Field(..., description="Title of the chapter")
    text: str = Field(..., description="Contents of the chapter")

# Course schema


class CourseSchema(BaseModel):
    name: str = Field(..., description="Title of the course")
    date: int = Field(..., description="Creation date as a unix timestamp")
    description: str = Field(..., description="Description of the course")
    domain: List[str] = Field(..., description="List of the course domain(s)")
    chapters: List[ChapterSchema] = Field(...,
                                          description="List of the course chapters")


class RateResponseSchema(BaseModel):
    message: str = Field(..., description="Response message")
    rating: int = Field(..., description="Total rating for the chapter")

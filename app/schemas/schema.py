from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List


class ChapterSchema(BaseModel):
    title: str = Field(..., description="Title of the chapter")
    contents: str = Field(..., description="Contents of the chapter")


class CourseSchema(BaseModel):
    name: str = Field(..., description="Title of the course")
    date: int = Field(..., description="Creation date as a unix timestamp")
    description: str = Field(..., description="Description of the course")
    domain: List[str] = Field(..., description="List of the course domain(s)")
    chapters: List[ChapterSchema] = Field(...,
                                          description="List of the course chapters")


class RateResponseSchema(BaseModel):
    message: str

# app/models/course_model.py

from pydantic import BaseModel
from typing import List, Optional


class Chapter(BaseModel):
    id: str
    name: str
    text: str


class Course(BaseModel):
    id: str
    name: str
    date: int  # Timestamp for date
    description: str
    domain: List[str]
    chapters: List[Chapter]
    total_rating: Optional[int] = 0

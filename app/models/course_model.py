# Pydantic models for request/response
from typing import List
from pydantic import BaseModel


class Chapter(BaseModel):
    name: str
    content: str


class Course(BaseModel):
    id: str
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]
    total_rating: int = 0

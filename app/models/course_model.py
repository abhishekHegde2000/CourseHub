from typing import List
from pydantic import BaseModel, Field


class Chapter(BaseModel):
    name: str
    text: str


class Course(BaseModel):
    id: str
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]
    total_rating: int = 0

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# Library schemas
class LibraryGameAdd(BaseModel):
    igdb_id: int


class LibraryGameResponse(BaseModel):
    id: int
    igdb_id: int
    name: str
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    release_date: Optional[datetime] = None
    added_at: datetime

    class Config:
        from_attributes = True


class LibraryGameListResponse(BaseModel):
    games: list[LibraryGameResponse]
    total: int
    page: int
    page_size: int

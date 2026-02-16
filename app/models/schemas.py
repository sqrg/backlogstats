from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Auth schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# User schemas
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
    platform_igdb_id: int
    platform_name: str


class LibraryGameResponse(BaseModel):
    id: int
    igdb_id: int
    name: str
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    release_date: Optional[datetime] = None
    platform_igdb_id: int
    platform_name: str
    added_at: datetime

    class Config:
        from_attributes = True


class LibraryGameListResponse(BaseModel):
    games: list[LibraryGameResponse]
    total: int
    page: int
    page_size: int

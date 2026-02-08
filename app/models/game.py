from pydantic import BaseModel
from typing import Optional


class Platform(BaseModel):
    id: int
    name: str


class ReleaseDate(BaseModel):
    date: Optional[int] = None
    human: Optional[str] = None
    platform: Optional[Platform] = None


class Cover(BaseModel):
    url_1080p: Optional[str] = None
    url_720p: Optional[str] = None
    url_cover_big: Optional[str] = None
    image_id: Optional[str] = None


class Genre(BaseModel):
    id: int
    name: str


class Company(BaseModel):
    id: int
    name: str


class InvolvedCompany(BaseModel):
    company: Company
    developer: bool = False
    publisher: bool = False


class Game(BaseModel):
    id: int
    name: str
    platforms: Optional[list[Platform]] = None
    release_dates: Optional[list[ReleaseDate]] = None
    cover: Optional[Cover] = None
    summary: Optional[str] = None
    storyline: Optional[str] = None
    genres: Optional[list[Genre]] = None
    involved_companies: Optional[list[InvolvedCompany]] = None
    rating: Optional[float] = None
    aggregated_rating: Optional[float] = None

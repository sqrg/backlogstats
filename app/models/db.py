from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """User model for storing user accounts."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    library_games: list["UserGame"] = Relationship(back_populates="user")


class GameCache(SQLModel, table=True):
    """Local cache of game data from IGDB to reduce API calls."""

    __tablename__ = "games_cache"

    id: Optional[int] = Field(default=None, primary_key=True)
    igdb_id: int = Field(unique=True, index=True)
    name: str = Field(index=True)
    summary: Optional[str] = None
    cover_url: Optional[str] = None
    release_date: Optional[datetime] = None
    cached_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user_games: list["UserGame"] = Relationship(back_populates="game")


class UserGame(SQLModel, table=True):
    """Join table linking users to their game library."""

    __tablename__ = "user_games"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    game_id: int = Field(foreign_key="games_cache.id", index=True)
    igdb_id: int = Field(index=True)  # Store IGDB ID for quick lookups
    added_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="library_games")
    game: Optional[GameCache] = Relationship(back_populates="user_games")

    class Config:
        # Ensure unique constraint on user_id + game_id
        pass

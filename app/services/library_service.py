from sqlmodel import Session, select
from typing import Optional
from datetime import datetime

from app.models.db import User, GameCache, UserGame
from app.services.igdb_service import igdb_service


class LibraryService:
    async def get_or_create_user(self, session: Session, user_id: int) -> Optional[User]:
        """Get user by ID. For Phase 1, we create a default user if none exists."""
        user = session.get(User, user_id)
        return user

    async def create_default_user(self, session: Session) -> User:
        """Create a default user for Phase 1 (before auth is implemented)."""
        user = User(username="default", email="default@backlogstats.local")
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    async def get_or_create_default_user(self, session: Session) -> User:
        """Get or create the default user for Phase 1."""
        statement = select(User).where(User.username == "default")
        user = session.exec(statement).first()
        if not user:
            user = await self.create_default_user(session)
        return user

    async def get_or_cache_game(self, session: Session, igdb_id: int) -> GameCache:
        """Get game from cache or fetch from IGDB and cache it."""
        statement = select(GameCache).where(GameCache.igdb_id == igdb_id)
        cached_game = session.exec(statement).first()

        if cached_game:
            return cached_game

        # Fetch from IGDB
        igdb_game = await igdb_service.get_game_by_id(igdb_id)
        if not igdb_game:
            raise ValueError(f"Game with IGDB ID {igdb_id} not found")

        # Parse release date
        release_date = None
        if igdb_game.get("release_dates"):
            first_release = igdb_game["release_dates"][0]
            if first_release.get("date"):
                release_date = datetime.fromtimestamp(first_release["date"])

        # Get cover URL
        cover_url = None
        if igdb_game.get("cover"):
            cover_url = igdb_game["cover"].get("url_720p")

        # Create cache entry
        game_cache = GameCache(
            igdb_id=igdb_id,
            name=igdb_game["name"],
            summary=igdb_game.get("summary"),
            cover_url=cover_url,
            release_date=release_date,
        )
        session.add(game_cache)
        session.commit()
        session.refresh(game_cache)
        return game_cache

    async def add_game_to_library(
        self, session: Session, user_id: int, igdb_id: int
    ) -> UserGame:
        """Add a game to user's library."""
        # Check if already in library
        statement = select(UserGame).where(
            UserGame.user_id == user_id, UserGame.igdb_id == igdb_id
        )
        existing = session.exec(statement).first()
        if existing:
            raise ValueError("Game already in library")

        # Get or cache the game
        game_cache = await self.get_or_cache_game(session, igdb_id)

        # Create library entry
        user_game = UserGame(
            user_id=user_id,
            game_id=game_cache.id,
            igdb_id=igdb_id,
        )
        session.add(user_game)
        session.commit()
        session.refresh(user_game)
        return user_game

    def get_library_games(
        self,
        session: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[UserGame], int]:
        """Get paginated list of games in user's library."""
        # Count total
        count_statement = select(UserGame).where(UserGame.user_id == user_id)
        total = len(session.exec(count_statement).all())

        # Get paginated results
        offset = (page - 1) * page_size
        statement = (
            select(UserGame)
            .where(UserGame.user_id == user_id)
            .offset(offset)
            .limit(page_size)
        )
        games = session.exec(statement).all()
        return list(games), total

    def get_library_game(
        self, session: Session, user_id: int, igdb_id: int
    ) -> Optional[UserGame]:
        """Get a specific game from user's library by IGDB ID."""
        statement = select(UserGame).where(
            UserGame.user_id == user_id, UserGame.igdb_id == igdb_id
        )
        return session.exec(statement).first()

    def remove_from_library(
        self, session: Session, user_id: int, igdb_id: int
    ) -> bool:
        """Remove a game from user's library."""
        statement = select(UserGame).where(
            UserGame.user_id == user_id, UserGame.igdb_id == igdb_id
        )
        user_game = session.exec(statement).first()
        if not user_game:
            return False

        session.delete(user_game)
        session.commit()
        return True


# Singleton instance
library_service = LibraryService()

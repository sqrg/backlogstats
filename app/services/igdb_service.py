import httpx
import os
from typing import Optional
from datetime import datetime, timedelta


class IGDBService:
    def __init__(self):
        self.client_id = os.getenv("IGDB_CLIENT_ID")
        self.client_secret = os.getenv("IGDB_CLIENT_SECRET")
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.base_url = "https://api.igdb.com/v4"
        self.auth_url = "https://id.twitch.tv/oauth2/token"

    async def _get_access_token(self) -> str:
        """Get OAuth2 access token from Twitch."""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.auth_url,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            return self.access_token

    async def search_games(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for games by name.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of game dictionaries with id, name, platforms, release dates, and cover image
        """
        token = await self._get_access_token()

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}",
        }

        # IGDB uses a specific query language
        # We're requesting: name, platforms (with names), release_dates (with human-readable format), and cover image
        body = f"""
        search "{query}";
        fields name, platforms.name, release_dates.date, release_dates.human, release_dates.platform.name, cover.image_id;
        limit {limit};
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/games",
                headers=headers,
                data=body,
            )
            response.raise_for_status()
            results = response.json()

            # Process results to add cover URLs in multiple sizes
            for game in results:
                if "cover" in game and "image_id" in game["cover"]:
                    image_id = game["cover"]["image_id"]
                    # Construct URLs for different sizes
                    game["cover"]["url_1080p"] = f"https://images.igdb.com/igdb/image/upload/t_1080p/{image_id}.jpg"
                    game["cover"]["url_720p"] = f"https://images.igdb.com/igdb/image/upload/t_720p/{image_id}.jpg"
                    game["cover"]["url_cover_big"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"

            return results

    async def get_game_by_id(self, game_id: int) -> dict:
        """
        Get detailed information for a specific game by ID.

        Args:
            game_id: The IGDB game ID

        Returns:
            Game dictionary with detailed information including summary, genres, companies, screenshots, etc.
        """
        token = await self._get_access_token()

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}",
        }

        # Request comprehensive game data
        body = f"""
        fields name, summary, storyline, platforms.name, release_dates.date, release_dates.human,
               release_dates.platform.name, cover.image_id, genres.name, involved_companies.company.name,
               involved_companies.developer, involved_companies.publisher,
               rating, aggregated_rating;
        where id = {game_id};
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/games",
                headers=headers,
                data=body,
            )
            response.raise_for_status()
            results = response.json()

            if not results:
                return None

            game = results[0]

            # Process cover URLs
            if "cover" in game and "image_id" in game["cover"]:
                image_id = game["cover"]["image_id"]
                game["cover"]["url_1080p"] = f"https://images.igdb.com/igdb/image/upload/t_1080p/{image_id}.jpg"
                game["cover"]["url_720p"] = f"https://images.igdb.com/igdb/image/upload/t_720p/{image_id}.jpg"
                game["cover"]["url_cover_big"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"

            return game


# Create a singleton instance
igdb_service = IGDBService()

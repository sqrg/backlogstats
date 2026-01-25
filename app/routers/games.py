from fastapi import APIRouter, Query, HTTPException, Path
from app.services.igdb_service import igdb_service
from app.models.game import Game

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/search", response_model=list[Game])
async def search_games(
    q: str = Query(..., description="Search query for game name", min_length=1),
    limit: int = Query(10, description="Maximum number of results", ge=1, le=50),
):
    """
    Search for games by name using the IGDB API.

    Returns a list of games with their name, platforms, release dates, and cover images.
    """
    try:
        results = await igdb_service.search_games(query=q, limit=limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching games: {str(e)}")


@router.get("/{game_id}", response_model=Game)
async def get_game(
    game_id: int = Path(..., description="The IGDB game ID", gt=0),
):
    """
    Get detailed information for a specific game by ID.

    Returns comprehensive game data including summary, genres, developers,
    publishers, screenshots, videos, and ratings.
    """
    try:
        game = await igdb_service.get_game_by_id(game_id=game_id)
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with ID {game_id} not found")
        return game
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching game details: {str(e)}")

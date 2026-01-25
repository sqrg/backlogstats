from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from app.core.database import get_session
from app.services.library_service import library_service
from app.models.schemas import (
    LibraryGameAdd,
    LibraryGameResponse,
    LibraryGameListResponse,
)

router = APIRouter(prefix="/library", tags=["library"])


async def get_current_user_id(session: Session = Depends(get_session)) -> int:
    """
    Get current user ID. For Phase 1, returns the default user.
    Will be replaced with actual auth in Phase 2.
    """
    user = await library_service.get_or_create_default_user(session)
    return user.id


@router.post("/games", response_model=LibraryGameResponse, status_code=201)
async def add_game_to_library(
    game: LibraryGameAdd,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    """
    Add a game to your personal library.

    Fetches game data from IGDB and stores it in your library.
    """
    try:
        user_game = await library_service.add_game_to_library(
            session=session,
            user_id=user_id,
            igdb_id=game.igdb_id,
        )
        # Load the game cache for response
        game_cache = user_game.game
        return LibraryGameResponse(
            id=user_game.id,
            igdb_id=user_game.igdb_id,
            name=game_cache.name,
            summary=game_cache.summary,
            cover_url=game_cache.cover_url,
            release_date=game_cache.release_date,
            added_at=user_game.added_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding game: {str(e)}")


@router.get("/games", response_model=LibraryGameListResponse)
async def list_library_games(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    """
    List all games in your personal library with pagination.
    """
    user_games, total = library_service.get_library_games(
        session=session,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

    games = []
    for user_game in user_games:
        game_cache = user_game.game
        games.append(
            LibraryGameResponse(
                id=user_game.id,
                igdb_id=user_game.igdb_id,
                name=game_cache.name,
                summary=game_cache.summary,
                cover_url=game_cache.cover_url,
                release_date=game_cache.release_date,
                added_at=user_game.added_at,
            )
        )

    return LibraryGameListResponse(
        games=games,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/games/{igdb_id}", response_model=LibraryGameResponse)
async def get_library_game(
    igdb_id: int = Path(..., description="IGDB game ID", gt=0),
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    """
    Get a specific game from your library by IGDB ID.
    """
    user_game = library_service.get_library_game(
        session=session,
        user_id=user_id,
        igdb_id=igdb_id,
    )

    if not user_game:
        raise HTTPException(status_code=404, detail="Game not found in library")

    game_cache = user_game.game
    return LibraryGameResponse(
        id=user_game.id,
        igdb_id=user_game.igdb_id,
        name=game_cache.name,
        summary=game_cache.summary,
        cover_url=game_cache.cover_url,
        release_date=game_cache.release_date,
        added_at=user_game.added_at,
    )


@router.delete("/games/{igdb_id}", status_code=204)
async def remove_game_from_library(
    igdb_id: int = Path(..., description="IGDB game ID", gt=0),
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    """
    Remove a game from your personal library.
    """
    removed = library_service.remove_from_library(
        session=session,
        user_id=user_id,
        igdb_id=igdb_id,
    )

    if not removed:
        raise HTTPException(status_code=404, detail="Game not found in library")

    return None

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session

from app.core.database import get_session
from app.core.auth import get_current_user
from app.models.db import User
from app.services.library_service import library_service
from app.models.schemas import (
    LibraryGameAdd,
    LibraryGameResponse,
    LibraryGameListResponse,
)

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/games", response_model=LibraryGameResponse, status_code=201)
async def add_game_to_library(
    game: LibraryGameAdd,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Add a game to your collection for a specific platform.

    The same game can be added for different platforms.
    """
    try:
        user_game = await library_service.add_game_to_library(
            session=session,
            user_id=current_user.id,
            igdb_id=game.igdb_id,
            platform_igdb_id=game.platform_igdb_id,
            platform_name=game.platform_name,
        )
        game_cache = user_game.game
        return LibraryGameResponse(
            id=user_game.id,
            igdb_id=user_game.igdb_id,
            name=game_cache.name,
            summary=game_cache.summary,
            cover_url=game_cache.cover_url,
            release_date=game_cache.release_date,
            platform_igdb_id=user_game.platform_igdb_id,
            platform_name=user_game.platform_name,
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
    current_user: User = Depends(get_current_user),
):
    """
    List all games in your collection with pagination.
    """
    user_games, total = library_service.get_library_games(
        session=session,
        user_id=current_user.id,
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
                platform_igdb_id=user_game.platform_igdb_id,
                platform_name=user_game.platform_name,
                added_at=user_game.added_at,
            )
        )

    return LibraryGameListResponse(
        games=games,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/games/{igdb_id}", response_model=list[LibraryGameResponse])
async def get_library_game(
    igdb_id: int = Path(..., description="IGDB game ID", gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get all entries for a specific game in your collection (one per platform).
    """
    user_games = library_service.get_library_games_by_igdb_id(
        session=session,
        user_id=current_user.id,
        igdb_id=igdb_id,
    )

    if not user_games:
        raise HTTPException(status_code=404, detail="Game not found in collection")

    return [
        LibraryGameResponse(
            id=ug.id,
            igdb_id=ug.igdb_id,
            name=ug.game.name,
            summary=ug.game.summary,
            cover_url=ug.game.cover_url,
            release_date=ug.game.release_date,
            platform_igdb_id=ug.platform_igdb_id,
            platform_name=ug.platform_name,
            added_at=ug.added_at,
        )
        for ug in user_games
    ]


@router.delete("/games/{igdb_id}/platforms/{platform_igdb_id}", status_code=204)
async def remove_game_from_library(
    igdb_id: int = Path(..., description="IGDB game ID", gt=0),
    platform_igdb_id: int = Path(..., description="IGDB platform ID", gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a specific game+platform entry from your collection.
    """
    removed = library_service.remove_from_library(
        session=session,
        user_id=current_user.id,
        igdb_id=igdb_id,
        platform_igdb_id=platform_igdb_id,
    )

    if not removed:
        raise HTTPException(status_code=404, detail="Game not found in collection")

    return None

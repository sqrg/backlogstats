from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import auth, games, library
from app.core.database import create_db_and_tables

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup (for development)
    # In production, use Alembic migrations instead
    create_db_and_tables()
    yield


app = FastAPI(title="Backlog Stats API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(games.router)
app.include_router(library.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Backlog Stats API"}
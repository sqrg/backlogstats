from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import games

load_dotenv()

app = FastAPI(title="Backlog Stats API", version="0.1.0")

app.include_router(games.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Backlog Stats API"}
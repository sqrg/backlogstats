# Backlog Stats

A video game collection and backlog manager built with FastAPI and the IGDB API.

## Features

- **Game Search**: Search for games using the IGDB (Internet Game Database) API
- Returns game information including name, platforms, and release dates

## Prerequisites

- Python 3.9+
- IGDB API credentials (via Twitch Developer Console)

## Setup

### 1. Clone the repository

```bash
cd backlogstats
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn httpx python-dotenv
```

### 4. Get IGDB API Credentials

1. Go to [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Log in with your Twitch account (create one if needed)
3. Click "Register Your Application"
4. Fill in the form:
   - Name: Choose any name for your app
   - OAuth Redirect URLs: `http://localhost`
   - Category: Choose appropriate category
5. Click "Create"
6. Copy your **Client ID** and **Client Secret**

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:

```env
IGDB_CLIENT_ID=your_client_id_here
IGDB_CLIENT_SECRET=your_client_secret_here
```

## Running the Application

Start the development server:

```bash
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Search Games

Search for games by name.

**Endpoint:** `GET /games/search`

**Query Parameters:**
- `q` (required): Search query string
- `limit` (optional): Maximum number of results (default: 10, max: 50)

**Example Request:**

```bash
curl "http://localhost:8000/games/search?q=zelda&limit=5"
```

**Example Response:**

```json
[
  {
    "id": 1234,
    "name": "The Legend of Zelda: Breath of the Wild",
    "platforms": [
      {
        "id": 130,
        "name": "Nintendo Switch"
      },
      {
        "id": 41,
        "name": "Wii U"
      }
    ],
    "release_dates": [
      {
        "date": 1488499200,
        "human": "Mar 03, 2017"
      }
    ]
  }
]
```

## Project Structure

```
backlogstats/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── game.py            # Pydantic models for games
│   ├── routers/
│   │   ├── __init__.py
│   │   └── games.py           # Game-related endpoints
│   └── services/
│       ├── __init__.py
│       └── igdb_service.py    # IGDB API integration
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment variables template
└── README.md
```

## Development

The project uses:
- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for API requests
- **python-dotenv**: Environment variable management

## Roadmap

- [ ] Add user authentication
- [ ] Create game collections/libraries
- [ ] Track backlog status (to play, playing, completed)
- [ ] Add game ratings and reviews
- [ ] Statistics and analytics dashboard

## Resources

- [IGDB API Documentation](https://api-docs.igdb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Twitch Developer Console](https://dev.twitch.tv/console/apps)

## License

This project is for personal use.

# Spec-Driven AI App Builder - Backend

FastAPI backend for the Spec-Driven AI App Builder platform.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `SUPABASE_SERVICE_KEY`: Your Supabase service role key
- `SECRET_KEY`: Generate with `openssl rand -hex 32`

### 4. Set Up Supabase Database

Run the SQL migrations in `migrations/` folder in your Supabase SQL editor.

### 5. Run the Server

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Supabase client
│   ├── models.py            # Pydantic models
│   ├── auth.py              # Authentication utilities
│   └── routers/             # API route handlers
│       ├── auth.py          # Authentication endpoints
│       ├── projects.py      # Project management
│       ├── specs.py         # Specification files
│       ├── files.py         # Code files
│       ├── agents.py        # AI agents
│       ├── chat.py          # AI chat
│       ├── marketplace.py   # Component marketplace
│       └── subscription.py  # Subscription management
├── migrations/              # Database migrations
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Current Implementation Status

### ✅ Completed
- FastAPI application setup
- CORS middleware
- Authentication (signup, login, JWT)
- Project CRUD operations
- Spec file retrieval
- Subscription info endpoint
- Database models and schemas

### 🚧 In Progress / TODO
- Spec file versioning and rollback
- File management in sandboxes
- AI agent integration (Agno framework)
- Code change review workflow
- E2B sandbox integration
- AI chat functionality
- Marketplace implementation
- Polar payment integration
- Project memory system
- Deployment pipeline

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

For production deployment:

1. Set `reload=False` in uvicorn
2. Use a production ASGI server (gunicorn + uvicorn workers)
3. Set up proper environment variables
4. Configure CORS for your production domain
5. Enable HTTPS
6. Set up monitoring and logging

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

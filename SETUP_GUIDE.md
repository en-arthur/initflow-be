# Backend Setup Guide

Complete guide to set up and run the Spec-Driven AI App Builder backend.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Supabase account (free tier works)
- Git

## Step-by-Step Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Python-JOSE (JWT tokens)
- Passlib (password hashing)
- Supabase (database client)
- And other dependencies

### 4. Set Up Supabase

#### 4.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - Name: `spec-builder` (or your choice)
   - Database Password: (save this!)
   - Region: Choose closest to you
5. Wait for project to be created (~2 minutes)

#### 4.2 Get API Credentials

1. In your Supabase project dashboard
2. Go to Settings → API
3. Copy these values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public** key (under Project API keys)
   - **service_role** key (under Project API keys - keep this secret!)

#### 4.3 Run Database Migration

1. In Supabase dashboard, go to SQL Editor
2. Click "New Query"
3. Copy the entire contents of `migrations/001_initial_schema.sql`
4. Paste into the SQL editor
5. Click "Run" or press Ctrl+Enter
6. You should see "Success. No rows returned"

This creates all the necessary tables, indexes, and security policies.

### 5. Configure Environment Variables

#### 5.1 Copy Example File

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

#### 5.2 Edit .env File

Open `.env` in your text editor and fill in:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

# JWT Configuration
SECRET_KEY=generate_this_with_command_below
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# AI Configuration (optional for now)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# E2B Configuration (optional for now)
E2B_API_KEY=
```

#### 5.3 Generate Secret Key

**Windows (PowerShell):**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**Mac/Linux:**
```bash
openssl rand -hex 32
```

Copy the output and paste it as your `SECRET_KEY` in `.env`

### 6. Verify Setup

Run the test script:

```bash
python test_setup.py
```

You should see all checks pass:
```
✓ All checks passed! You're ready to run the backend.
```

If any checks fail, review the error messages and fix the issues.

### 7. Start the Server

**Option 1: Using run.py (recommended for development)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 8. Test the API

Open your browser and go to:

- **API Root:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

You should see the API documentation and be able to test endpoints.

### 9. Test Authentication

Using the Swagger UI at http://localhost:8000/docs:

1. Expand `POST /api/auth/signup`
2. Click "Try it out"
3. Enter test data:
   ```json
   {
     "email": "test@example.com",
     "password": "testpassword123",
     "name": "Test User"
   }
   ```
4. Click "Execute"
5. You should get a 201 response with a token

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Supabase Connection Errors

- Verify your `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check that your Supabase project is active
- Ensure you ran the database migration

### Port Already in Use

If port 8000 is already in use:
```bash
# Change port in .env
API_PORT=8001

# Or specify when running
uvicorn app.main:app --reload --port 8001
```

### CORS Errors from Frontend

Make sure `CORS_ORIGINS` in `.env` includes your frontend URL:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Next Steps

1. **Connect Frontend:** Update frontend `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
2. **Test Integration:** Try signing up from the frontend
3. **Implement Features:** Continue with remaining tasks (AI agents, sandboxes, etc.)

## Development Tips

### Auto-Reload

The server automatically reloads when you change code files. Just save and the changes take effect immediately.

### View Logs

All requests and errors are logged to the console. Watch for:
- Request logs: `INFO: "GET /api/projects HTTP/1.1" 200 OK`
- Error logs: `ERROR: ...`

### Database Queries

You can view and test database queries in Supabase:
1. Go to Table Editor to see data
2. Go to SQL Editor to run custom queries

### API Testing

Use the Swagger UI at `/docs` to test all endpoints without writing code.

## Production Deployment

For production:

1. Set `reload=False` in uvicorn
2. Use gunicorn with uvicorn workers
3. Set strong `SECRET_KEY`
4. Use environment-specific CORS origins
5. Enable HTTPS
6. Set up monitoring and logging
7. Use a production database

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Support

If you encounter issues:
1. Check the error messages carefully
2. Review this guide
3. Check Supabase dashboard for database issues
4. Verify all environment variables are set correctly

# Student Task Management API

A small FastAPI application using SQLAlchemy 2.x and SQLite. It includes a
health endpoint and an example endpoint that stores an item with a title and
created/updated timestamps.

## Requirements

- Python 3.10 or newer
- Dependencies listed in `requirements.txt`

## Set up

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the application

From the project root, run:

```bash
uvicorn app.main:app --reload
```

The service listens at `http://127.0.0.1:8000` by default. Interactive API
documentation is available at `/docs`.

### Endpoints

- `GET /health` returns `{"status": "ok"}`.
- `POST /items` accepts `{"title": "Example item"}` and returns the stored
  item, including its generated ID and timestamps.

The SQLite database defaults to `./app.db`. Set the `DATABASE_URL` environment
variable to use a different SQLAlchemy database URL. The database tables are
created when the application starts; for a production deployment, use
migrations rather than relying on `create_all`.

## Run tests

```bash
python -m pytest
```

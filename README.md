# Smart Expense Tracker API

A REST API for managing personal expenses, built with Python and FastAPI. Supports creating, listing, filtering, and deleting expenses, as well as viewing totals broken down by category. Data is persisted to a local JSON file — no database setup required.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Server

```bash
uvicorn src.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## Run Tests

```bash
pytest
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/expenses` | Add a new expense |
| GET | `/expenses` | List all expenses (optional `?category=` filter) |
| GET | `/expenses/total` | Get total spending overall and by category |
| DELETE | `/expenses/{id}` | Delete an expense by ID |

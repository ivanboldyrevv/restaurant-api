## Intro
This project is a REST API for the restaurant service layer. The service allows you to create, view and delete reservations, as well as manage tables and time slots. The system uses FastAPI, SQLAlchemy to work with the PostgreSQL database and is managed using Docker and docker-compose.

---
### Installation and run
```bash
git clone <url repository>
cd <project path>
```
```bash
docker compose up -d
docker exec restaurant_backend alembic revision --autogenerate -m "initial"
docker exec restaurant_backend alembic upgrade head
```
---
### Structure

- `routers/*` is a directory for storing API routes (for example, for tables and armor).
- `schemas/*` — Data schemas used for validation and serialization.
- `services/*` — Logic of interaction with the database and processing of business logic.
- `tests/*` — Tests to cover basic scenarios (using pytest).
- `container.py` - Container dependecies injection.
- `database.py` - Database connection.
- `exceptions.py` - Custom exception.
- `models.py` — Models for the database that define the structure of tables.
- `main.py` - Main file.

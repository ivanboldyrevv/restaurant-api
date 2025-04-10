### Setup project
```
docker compose up -d
docker exec restaurant_backend alembic revision --autogenerate -m "initial migration"
docker exec restaurant_backend alembic upgrade head
```
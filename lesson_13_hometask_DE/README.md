# ETL Pipeline - Lecture 13

## Run with Docker + PostgreSQL

```bash
# 1. Postgres + .ipynb (all in Docker)
docker compose up --build

# 2. Connect to Postgres manually (optional)
docker compose exec postgres psql -U etl -d etl_db

# 3. Stop the containers
docker compose down

# 4. Stop and remove Postgres data
docker compose down -v
```

## Run without Docker (SQLite)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Open the notebook
jupyter notebook lesson_13_pipeline.ipynb

# 3. Run all cells
#    PostgreSQL cells will fail with an error.
#    The SQLite cells at the bottom will run successfully and create data/etl.db.
```

#!/bin/bash

alembic upgrade head
uvicorn my_food.adapters.FastAPI.main:app --host 0.0.0.0 --port 8000 --reload

#!/bin/bash

alembic upgrade head
uvicorn src.infrastructure.FastAPI.main:app --host 0.0.0.0 --port 8000 --reload

#!/bin/bash

alembic upgrade head
uvicorn src.adapters.FastAPI.main:app --host 0.0.0.0 --port 8000 --reload

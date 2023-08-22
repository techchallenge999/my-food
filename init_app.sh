#!/bin/bash

alembic upgrade head
uvicorn src.infrastructure.fast_api.main:app --host 0.0.0.0 --port 8000 --reload

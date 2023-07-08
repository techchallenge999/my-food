import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from my_food.adapters.FastAPI.views.auth import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)

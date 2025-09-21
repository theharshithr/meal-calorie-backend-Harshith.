import pytest
from httpx import AsyncClient
from meal_backend_v2.app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register
        r = await ac.post("/auth/register", json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "strongpassword"
        })
        assert r.status_code == 201
        # login
        r2 = await ac.post("/auth/login", json={"email": "test@example.com", "password": "strongpassword"})
        assert r2.status_code == 200
        data = r2.json()
        assert "access_token" in data

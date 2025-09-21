import pytest
from httpx import AsyncClient
import respx
from meal_backend_v2.app.main import app

USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

@pytest.mark.asyncio
@respx.mock
async def test_get_calories_with_mocked_usda():
    mock_resp = {
        "foods": [
            {
                "description": "Grilled Salmon",
                "foodNutrients": [
                    {"nutrientName": "Energy", "value": 200}
                ],
                "servingSize": 100
            }
        ]
    }
    respx.get(USDA_URL).mock(return_value=respx.MockResponse(200, json=mock_resp))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json={"first_name":"A","last_name":"B","email":"m@x.com","password":"pw"})
        login = await ac.post("/auth/login", json={"email":"m@x.com","password":"pw"})
        token = login.json().get("access_token")

        r = await ac.post("/get-calories", json={"dish_name":"griled salmon","servings":2}, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        data = r.json()
        assert data["calories_per_serving"] == 200.0
        assert data["total_calories"] == 400.0

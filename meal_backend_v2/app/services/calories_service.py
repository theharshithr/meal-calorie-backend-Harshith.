from app.services.usda_client import USDAClient
from app.schemas.calories import CaloriesRequest, CaloriesResponse

class CaloriesService:
    def __init__(self, usda_client: USDAClient):
        self.usda = usda_client

    async def calculate(self, payload: CaloriesRequest) -> CaloriesResponse:
        if payload.servings <= 0:
            raise ValueError("Servings must be greater than 0")
        food = await self.usda.find_best_food(payload.dish_name)
        if not food:
            raise LookupError("Dish not found")
        kcal = await self.usda.get_calories_from_food(food)
        serving_size = food.get("servingSize") or None
        if serving_size and isinstance(serving_size, (int, float)) and serving_size > 0:
            cal_per_serving = kcal * (serving_size / 100.0)
        else:
            cal_per_serving = kcal
        total = cal_per_serving * payload.servings
        total = float(round(total, 2))
        cal_per_serving = float(round(cal_per_serving, 2))
        return CaloriesResponse(
            dish_name=payload.dish_name,
            servings=payload.servings,
            calories_per_serving=cal_per_serving,
            total_calories=total,
            source="USDA FoodData Central",
            ingredients=None
        )

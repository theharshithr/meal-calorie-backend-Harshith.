from pydantic import BaseModel
from typing import List, Optional

class IngredientBreakdown(BaseModel):
    name: str
    calories: Optional[float] = None

class CaloriesRequest(BaseModel):
    dish_name: str
    servings: float

class CaloriesResponse(BaseModel):
    dish_name: str
    servings: float
    calories_per_serving: float
    total_calories: float
    source: str
    ingredients: Optional[List[IngredientBreakdown]] = None

import httpx
from app.core.config import settings
from typing import Optional, Dict, Any, List, Tuple
from rapidfuzz import fuzz

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

class USDAClient:
    def __init__(self, api_key: str = settings.USDA_API_KEY):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10)

    async def _search(self, query: str, page_size: int = 10) -> Dict[str, Any]:
        params = {"query": query, "pageSize": page_size, "api_key": self.api_key}
        resp = await self.client.get(USDA_SEARCH_URL, params=params)
        resp.raise_for_status()
        return resp.json()

    def _best_local_fuzzy(self, query: str, candidates: List[Dict]) -> Optional[Tuple[Dict, int]]:
        best = None
        best_score = -1
        q = query.lower()
        for c in candidates:
            desc = (c.get("description") or c.get("lowercaseDescription") or "").lower()
            score = fuzz.partial_ratio(q, desc)
            if score > best_score:
                best_score = score
                best = c
        if best is None:
            return None
        return best, best_score

    async def find_best_food(self, query: str) -> Optional[Dict]:
        data = await self._search(query)
        foods = data.get("foods", [])
        if not foods:
            return None
        qlower = query.lower()
        for f in foods:
            if qlower in (f.get("description") or "").lower():
                return f
        fuzzy = self._best_local_fuzzy(query, foods)
        if fuzzy:
            best, score = fuzzy
            if score >= 30:
                return best
        return foods[0]

    async def get_calories_from_food(self, food: Dict) -> float:
        nutrients = food.get("foodNutrients") or food.get("foodNutrients", [])
        kcal = None
        for n in nutrients:
            name = n.get("nutrientName") or n.get("name") or ""
            if "energy" in name.lower() or "calorie" in name.lower():
                kcal = n.get("value") or n.get("amount") or n.get("value")
                break
        if kcal is None:
            label = food.get("labelNutrients") or {}
            if isinstance(label, dict):
                energy = label.get("calories") or label.get("energy")
                if energy and isinstance(energy, dict):
                    kcal = energy.get("value")
        return float(kcal) if kcal is not None else 0.0

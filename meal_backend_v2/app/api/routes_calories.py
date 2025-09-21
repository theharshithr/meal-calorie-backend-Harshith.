from fastapi import APIRouter, Header, HTTPException, status, Request, Depends
from app.schemas.calories import CaloriesRequest, CaloriesResponse
from app.services.usda_client import USDAClient
from app.services.calories_service import CaloriesService
from app.core.security import Security
from app.core.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

# This router is initialized without the 'security' parameter
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Dependency to handle token verification
def verify_auth_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        Security.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Return a success message or some value if verification passes
    return "Token verified"

# The security parameter is removed from the decorator, and a dependency is used instead
@router.post("/get-calories", response_model=CaloriesResponse)
@limiter.limit(settings.RATE_LIMIT)
async def get_calories(request: Request, payload: CaloriesRequest, token_status: str = Depends(verify_auth_token)):
    if payload.servings <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Servings must be > 0")

    usda = USDAClient()
    service = CaloriesService(usda)
    try:
        result = await service.calculate(payload)
    except LookupError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://mealuser:mealpass@db:5432/mealdb"
    USDA_API_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    RATE_LIMIT: str = "15/minute"

    class Config:
        env_file = ".env"

settings = Settings()

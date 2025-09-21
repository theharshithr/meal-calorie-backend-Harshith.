from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

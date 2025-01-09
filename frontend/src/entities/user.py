from pydantic import BaseModel, Field
from enum import Enum


class Role(str, Enum):
    DEVELOPER = "developer"
    DESIGNER = "designer"
    MANAGER = "manager"
    PRODUCT = "product"
    BUSINESS_DEVELOPMENT = "business_development"


class User(BaseModel):
    id: str = Field(..., description="Unique identifier for the user")
    name: str
    email: str
    role: Role

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import List


class Settings(BaseModel):
    duplicate_threshold: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Similarity threshold for duplication detection",
    )
    max_ticket_size: int = Field(
        default=2000, ge=100, description="Character limit before suggesting split"
    )


class Project(BaseModel):
    id: str = Field(..., description="Unique identifier for the project")
    name: str = Field(..., min_length=1, max_length=100)
    members: List[str] = Field(default_factory=list, description="User IDs")

    settings: Settings = Field(default_factory=Settings)

    class Config:
        from_attributes = True

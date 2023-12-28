from enum import Enum
from pydantic import BaseModel
from typing import Optional, Union


class PetEnum(Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Category(BaseModel):
    id: int = None
    name: str = None


class Tags(BaseModel):
    id: int = None
    name: str = None


class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Category] = None
    name: Optional[str] = None
    photoUrls: Optional[list[str]] = None
    tags: Optional[list[Tags]] = None
    status: Union[PetEnum]


class Pets(BaseModel):
    """Doesn't work"""
    body: list[Optional[Pet]] = None


class UpdBody(BaseModel):
    code: int
    type: str
    message: str


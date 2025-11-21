from typing import Optional
from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    url: Optional[str] = None
    description: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class SourceRead(SourceBase):
    id: int

    class Config:
        orm_mode = True

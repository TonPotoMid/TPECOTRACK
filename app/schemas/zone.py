from typing import Optional
from pydantic import BaseModel


class ZoneBase(BaseModel):
    name: str
    postal_code: Optional[str] = None
    geom: Optional[str] = None


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    postal_code: Optional[str] = None
    geom: Optional[str] = None


class ZoneRead(ZoneBase):
    id: int

    class Config:
        orm_mode = True

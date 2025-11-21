from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class IndicatorBase(BaseModel):
    source_id: Optional[int]
    type: str
    value: float
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    zone_id: Optional[int] = None
    metadata_json: Optional[str] = None


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata_json: Optional[str] = None


class IndicatorRead(IndicatorBase):
    id: int

    class Config:
        orm_mode = True

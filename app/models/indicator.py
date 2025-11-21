from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    type = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    # 'metadata' is a reserved name on Declarative base (Base.metadata).
    # Use attribute name 'metadata_json' but keep the column name 'metadata' in DB.
    metadata_json = Column("metadata", Text, nullable=True)

    source = relationship("Source", backref="indicators")

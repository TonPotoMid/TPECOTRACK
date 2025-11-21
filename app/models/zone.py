from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    geom = Column(Text, nullable=True)  # optional WKT/GeoJSON

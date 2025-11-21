from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    description = Column(Text, nullable=True)

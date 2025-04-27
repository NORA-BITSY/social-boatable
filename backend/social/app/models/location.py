from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from backend.social.app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)

    posts = relationship("Post", back_populates="location")

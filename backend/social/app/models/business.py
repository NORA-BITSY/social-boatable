from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.social.app.database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    address = Column(String(200))

    reviews = relationship("Post", back_populates="business")

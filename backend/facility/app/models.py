from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.facility.app.database import Base

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)

    storage_units = relationship("StorageUnit", back_populates="facility")

class StorageUnit(Base):
    __tablename__ = "storage_units"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    unit_number = Column(String(20))
    type = Column(String(20))  # e.g., "indoor", "outdoor"
    capacity = Column(Float)  # e.g., length in feet

    facility = relationship("Facility", back_populates="storage_units")
    vessel = relationship("Vessel", back_populates="storage_unit", uselist=False)

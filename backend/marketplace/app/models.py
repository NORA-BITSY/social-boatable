from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.marketplace.app.database import Base
import enum

class ServiceCategory(str, enum.Enum):
    maintenance = "Maintenance"
    repair = "Repair"
    cleaning = "Cleaning"
    training = "Training"

class ServiceListing(Base):
    __tablename__ = "service_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(Text)
    category = Column(Enum(ServiceCategory), nullable=False)
    price = Column(Float, nullable=True)
    provider_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    provider_business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    orders = relationship("ServiceOrder", back_populates="service")

class ProductListing(Base):
    __tablename__ = "product_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # e.g., "Boat", "Accessory"
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="active")  # e.g., "active", "sold"

class ServiceOrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"

class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("service_listings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Integer, default=1)
    total = Column(Float)
    status = Column(Enum(ServiceOrderStatus), default=ServiceOrderStatus.pending)

    service = relationship("ServiceListing", back_populates="orders")

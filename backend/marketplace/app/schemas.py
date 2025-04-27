from pydantic import BaseModel
from enum import Enum

class ServiceCategory(str, Enum):
    maintenance = "Maintenance"
    repair = "Repair"
    cleaning = "Cleaning"
    training = "Training"

class ServiceBase(BaseModel):
    title: str
    description: str | None = None
    category: ServiceCategory
    price: float | None = None

class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    service_id: int
    quantity: int = 1

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    total: float | None = None
    status: str

    class Config:
        orm_mode = True

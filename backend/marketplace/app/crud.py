from sqlalchemy.orm import Session
from . import models, schemas

# --- Service CRUD

def create_service(db: Session, svc: schemas.ServiceCreate, provider_id: int):
    db_svc = models.ServiceListing(**svc.dict(), provider_id=provider_id)
    db.add(db_svc)
    db.commit()
    db.refresh(db_svc)
    return db_svc


def list_services(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.ServiceListing).offset(skip).limit(limit).all()

# --- Product CRUD

def create_product(db: Session, product_data: schemas.ProductCreate, seller_id: int):
    db_product = models.ProductListing(
        title=product_data.title,
        description=product_data.description,
        category=product_data.category,
        price=product_data.price,
        seller_id=seller_id,
        status="active"
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductListing)\
             .filter(models.ProductListing.status == "active")\
             .offset(skip).limit(limit).all()

# --- Order CRUD

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    svc = db.query(models.ServiceListing).get(order.service_id)
    if svc is None:
        raise ValueError("Service not found")
    total = (svc.price or 0) * order.quantity
    db_order = models.ServiceOrder(
        service_id=svc.id,
        user_id=user_id,
        quantity=order.quantity,
        total=total,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def list_orders_by_user(db: Session, user_id: int):
    return db.query(models.ServiceOrder).filter(models.ServiceOrder.user_id == user_id).all()

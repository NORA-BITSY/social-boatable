from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from backend.social.app.dependencies import get_current_user, get_db

router = APIRouter()

@router.post("/", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_product = crud.create_product(db, product, seller_id=current_user.id)
    return new_product

@router.get("/", response_model=list[schemas.ProductRead])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    products = crud.list_products(db, skip=skip, limit=limit)
    return products

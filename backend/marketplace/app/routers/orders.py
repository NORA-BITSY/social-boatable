from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from backend.social.app.dependencies import get_current_user, get_db

router = APIRouter()

@router.get("/")
async def read_orders():
    return [{"service_id": 1, "quantity": 2}, {"service_id": 2, "quantity": 1}]

@router.get("/{order_id}")
async def read_order(order_id: int):
    return {"order_id": order_id}

@router.get("/my", response_model=list[schemas.OrderRead])
async def my_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.list_orders_by_user(db, current_user.id)

@router.post("/", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
async def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return crud.create_order(db, order, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

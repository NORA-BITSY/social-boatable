from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    message: schemas.MessageCreate,
    receiver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔒 protected
):
    db_message = crud.create_message(db, message, sender_id=current_user.id, receiver_id=receiver_id)
    crud.create_notification(db, receiver_id, "message", f"New message from {current_user.username}")
    return db_message

@router.get("/", response_model=list[schemas.MessageRead])
async def read_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_messages(db, skip=skip, limit=limit)

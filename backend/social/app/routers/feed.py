from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=list[schemas.PostRead])
def my_feed(limit: int = 20, db: Session = Depends(get_db),
            current=Depends(get_current_user)):
    ids = [u.id for u in current.following] + [current.id]
    return (db.query(models.Post)
              .filter(models.Post.user_id.in_(ids))
              .order_by(models.Post.created_at.desc())
              .limit(limit).all())

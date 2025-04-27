from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.create_post(db, post, user_id=current_user.id)

@router.get("/", response_model=list[schemas.PostRead])
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_posts(db, skip=skip, limit=limit)

@router.post("/comments/", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: schemas.CommentCreate,
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.create_comment(db, comment, user_id=current_user.id, post_id=post_id)

@router.get("/comments/", response_model=list[schemas.CommentRead])
async def read_comments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_comments(db, skip=skip, limit=limit)

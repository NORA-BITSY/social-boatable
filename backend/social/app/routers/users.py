from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()


@router.get("/", response_model=list[schemas.UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserRead)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.post("/{user_id}/vessels/", response_model=schemas.VesselRead, status_code=status.HTTP_201_CREATED)
async def create_vessel(
    user_id: int,
    vessel: schemas.VesselCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.create_vessel(db, vessel, user_id=user_id)

@router.get("/vessels/", response_model=list[schemas.VesselRead])
async def read_vessels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_vessels(db, skip=skip, limit=limit)

@router.post("/{user_id}/follow")
async def follow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    crud.follow_user(db, current_user.id, user_id)
    return {"message": "Followed successfully"}

@router.post("/{user_id}/unfollow")
async def unfollow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    crud.unfollow_user(db, current_user.id, user_id)
    return {"message": "Unfollowed successfully"}

@router.get("/feed", response_model=list[schemas.PostRead])
async def feed(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    posts = crud.get_feed(db, current_user.id, skip, limit)
    return posts

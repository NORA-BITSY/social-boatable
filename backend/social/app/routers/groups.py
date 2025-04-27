from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=list[schemas.GroupRead])
async def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    return crud.get_groups(db, skip=skip, limit=limit)

@router.get("/{name}", response_model=schemas.GroupRead)
async def read_group(
    name: str,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),  # 🔒 protected
):
    grp = crud.get_group(db, name)
    if not grp:
        raise HTTPException(status_code=404, detail="Group not found")
    return grp

@router.post("/", response_model=schemas.GroupRead, status_code=status.HTTP_201_CREATED)
async def create_group(
    group: schemas.GroupCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return crud.create_group(db, group)

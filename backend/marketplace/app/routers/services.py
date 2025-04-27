from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from backend.social.app.dependencies import get_current_user, get_db, role_required

router = APIRouter()


@router.get("/", response_model=list[schemas.ServiceRead])
async def read_services(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_services(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.ServiceRead, status_code=status.HTTP_201_CREATED)
async def create_service(
    svc: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("MECHANIC", "VENDOR")),
):
    return crud.create_service(db, svc, provider_id=current_user.id)

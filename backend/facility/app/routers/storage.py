from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models

router = APIRouter()

@router.get("/")
async def read_storage_units(db: Session = Depends(get_db)):
    units = db.query(models.StorageUnit).all()
    return units

@router.get("/{unit_id}")
async def read_storage_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(models.StorageUnit).get(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    return unit

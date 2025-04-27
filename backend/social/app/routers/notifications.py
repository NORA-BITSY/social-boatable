from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db, get_current_user
from sse_starlette import EventSourceResponse
import asyncio  # <-- added import

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=list[schemas.NotificationRead])
async def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_notifications(db, current_user.id, skip, limit)

@router.get("/stream", response_class=EventSourceResponse)
async def stream_notifications(request: Request, current=Depends(get_current_user), db: Session = Depends(get_db)):
    while True:
        if await request.is_disconnected():
            break
        unseen = crud.get_notifications(db, current.id, 0, 10)
        for n in unseen:
            yield {"event": n.type, "data": n.content}
            n.is_read = True
        db.commit()
        await asyncio.sleep(3)

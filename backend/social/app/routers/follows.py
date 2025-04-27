from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user
from backend.common.graph import record_follow

router = APIRouter(prefix="/users")

@router.post("/{username}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow(username: str, db: Session = Depends(get_db),
                 current=Depends(get_current_user)):
    target = crud.get_user_by_username(db, username)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if target.id == current.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    current.following.append(target)
    db.commit()
    record_follow(current.id, target.id)
    # Create a notification for the followed user
    crud.create_notification(db, target.id, "follow", f"{current.username} followed you!")
    return

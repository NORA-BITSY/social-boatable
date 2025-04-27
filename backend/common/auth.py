from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.social.app.security import SECRET_KEY, ALGORITHM, get_user_by_id
from backend.common.database import SessionLocal  # sync

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int | None = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db, uid)
    if user is None:
        raise credentials_exception
    return user

def role_required(*allowed: str):
    def guard(current=Depends(get_current_user)):
        if not set(current.roles or []).intersection(allowed):
            raise HTTPException(status_code=403, detail="Forbidden")
        return current
    return guard

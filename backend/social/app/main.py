from fastapi import FastAPI, Request
from .routers import users, groups, follows, feed, messages, notifications, auth

# NEW ➜ ensure ORM tables are present on startup
from .database import Base, engine          # noqa: E402  (after import path set-up)
from . import models as _social_models      # noqa: F401  (model registration)

# Rate-limit
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Boatable Social Service")
app.state.limiter = limiter
app.add_exception_handler(StarletteHTTPException, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(follows.router, prefix="/follows", tags=["follows"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(auth.router)

@app.on_event("startup")
def _init_tables() -> None:                 # 🔑
    """Create (or verify) social-schema tables at boot."""
    Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/feed/")
@limiter.limit("30/minute")
async def read_feed(request: Request):
    return {"message": "Hello Feed"}

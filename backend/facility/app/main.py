from fastapi import FastAPI
from .routers import storage, transport
from backend.common.database import SYNC_ENGINE as engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Boatable Facility Service")

app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(transport.router, prefix="/transport", tags=["transport"])

@app.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import FastAPI
from .routers import services, orders

# NEW imports – pull in social models so FK → users.id resolves
from backend.social.app.database import Base as SocialBase
from backend.social.app import models as _social_models   # noqa: F401

from .database import engine, Base as MarketplaceBase
from . import models as _market_models                    # noqa: F401

app = FastAPI(title="Boatable Marketplace Service")

app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])


@app.on_event("startup")
def _init_tables() -> None:            # 🔑 make sure BOTH schemas exist
    SocialBase.metadata.create_all(bind=engine)
    MarketplaceBase.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    return {"status": "ok"}

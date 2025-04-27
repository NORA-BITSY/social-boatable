from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def recommendations():
    return [{"item_id": 1, "item_type": "service", "reason": "Popular this week"}]

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_transport_jobs():
    return [{"origin": "Miami", "destination": "Bahamas"}, {"origin": "Key West", "destination": "Cuba"}]

@router.get("/{job_id}")
async def read_transport_job(job_id: int):
    return {"job_id": job_id}

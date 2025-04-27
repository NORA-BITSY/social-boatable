from fastapi import FastAPI
from .assistants import chat, recommendations

app = FastAPI(title="Boatable AI Service")

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/health")
async def health():
    return {"status": "ok"}

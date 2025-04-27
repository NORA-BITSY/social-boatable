from fastapi import APIRouter
import openai
from backend.common.config import get_settings

router = APIRouter()
settings = get_settings()
openai.api_key = settings.openai_api_key

@router.post("/")
async def chat(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return {"response": response.choices[0].message.content}

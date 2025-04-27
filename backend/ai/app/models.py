from pydantic import BaseModel

class Message(BaseModel):
    text: str
    sender: str

class Recommendation(BaseModel):
    item_id: int
    item_type: str
    reason: str

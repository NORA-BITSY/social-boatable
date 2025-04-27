from pydantic import BaseModel

class TransportJob(BaseModel):
    id: int
    origin: str
    destination: str

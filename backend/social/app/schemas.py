from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class PostType(str, Enum):
    status = "status"
    checkin = "checkin"
    review = "review"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_pic_url: Optional[str] = None
    home_port: Optional[str] = None
    boating_experience: Optional[str] = None
    privacy_settings: Optional[Dict] = None
    roles: Optional[List[str]] = None
    member_tier: str = "FREE"
    loyalty_points: int = 0

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

class VesselBase(BaseModel):
    name: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    length: Optional[float] = None
    storage_unit_id: Optional[int] = None

class VesselCreate(VesselBase):
    pass

class VesselRead(VesselBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    privacy: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    content: str
    privacy: Optional[str] = None
    type: PostType
    sponsored: bool = False
    group_id: Optional[int] = None
    location_id: Optional[int] = None
    business_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class BusinessBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None

class BusinessCreate(BusinessBase):
    pass

class BusinessRead(BusinessBase):
    id: int
    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int
    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class NotificationRead(BaseModel):
    id: int
    type: str
    content: str
    created_at: datetime
    is_read: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[int] = None

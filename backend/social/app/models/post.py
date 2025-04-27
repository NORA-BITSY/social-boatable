from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.social.app.database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    privacy = Column(String(20))  # e.g., "public", "followers", "group"
    type = Column(String(20))  # e.g., "status", "checkin", "review"
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)

    user = relationship("User", back_populates="posts")
    group = relationship("Group", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    location = relationship("Location", back_populates="posts")
    business = relationship("Business", back_populates="reviews")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

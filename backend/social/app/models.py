from sqlalchemy import Column, Integer, String, Text, ARRAY, JSON, ForeignKey, Float, Enum, DateTime, Boolean, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import relationship
from backend.social.app.database import Base
from sqlalchemy import Table
from datetime import datetime
import enum

# Association table for user follows
user_follows = Table(
    "user_follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followee_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("since", DateTime, default=datetime.utcnow),
    CheckConstraint("follower_id <> followee_id", name="ck_self_follow")
)
Index("ix_followed", user_follows.c.followee_id)

# Association table for user-group membership with roles
user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("role", String(20), default="member")
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    name = Column(String(100))
    bio = Column(Text)
    profile_pic_url = Column(String(200))
    home_port = Column(String(100))
    boating_experience = Column(String(50))
    privacy_settings = Column(JSON)
    roles = Column(ARRAY(String))
    member_tier = Column(String(20), default="FREE")
    loyalty_points = Column(Integer, default=0)
    groups = relationship("Group", secondary="user_group", back_populates="members")
    vessels = relationship("Vessel", back_populates="owner")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    following = relationship(
        "User",
        secondary=user_follows,
        primaryjoin=id==user_follows.c.follower_id,
        secondaryjoin=id==user_follows.c.followee_id,
        backref="followers",
    )
    notifications = relationship("Notification", back_populates="user")

class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    type = Column(String(20))
    length = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    storage_unit_id = Column(Integer, ForeignKey("storage_units.id"), nullable=True)
    owner = relationship("User", back_populates="vessels")
    storage_unit = relationship("StorageUnit", back_populates="vessel")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    privacy = Column(String(20), default="public")
    members = relationship("User", secondary="user_group", back_populates="groups")
    posts = relationship("Post", back_populates="group")

class PostType(str, enum.Enum):
    status = "status"
    checkin = "checkin"
    review = "review"

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    privacy = Column(String(20))
    type = Column(Enum(PostType))
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    sponsored = Column(Boolean, default=False)
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

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    address = Column(String(200))
    reviews = relationship("Post", back_populates="business")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    posts = relationship("Post", back_populates="location")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    user = relationship("User", back_populates="notifications")

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas
from passlib.hash import bcrypt
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = bcrypt.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        bio=user.bio,
        profile_pic_url=user.profile_pic_url,
        home_port=user.home_port,
        boating_experience=user.boating_experience,
        privacy_settings=user.privacy_settings,
        roles=user.roles,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def follow_user(db: Session, follower_id: int, followee_id: int):
    if follower_id == followee_id:
        raise ValueError("Cannot follow oneself")
    db.execute(models.user_follows.insert().values(follower_id=follower_id, followee_id=followee_id))
    db.commit()

def unfollow_user(db: Session, follower_id: int, followee_id: int):
    db.execute(models.user_follows.delete().where(
        and_(
            models.user_follows.c.follower_id == follower_id,
            models.user_follows.c.followee_id == followee_id
        )
    ))
    db.commit()

def get_feed(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    from backend.common.graph import followed_ids
    ids = followed_ids(user_id) | {user_id}
    return (db.query(models.Post)
              .filter(models.Post.user_id.in_(ids))
              .order_by(models.Post.created_at.desc())
              .limit(limit)
              .all())

def create_vessel(db: Session, vessel: schemas.VesselCreate, user_id: int) -> models.Vessel:
    db_vessel = models.Vessel(**vessel.dict(), owner_id=user_id)
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)
    return db_vessel

def get_vessels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vessel).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate, user_id: int) -> models.Post:
    db_post = models.Post(**post.dict(), user_id=user_id, created_at=datetime.utcnow())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, post_id: int) -> models.Comment:
    db_comment = models.Comment(**comment.dict(), user_id=user_id, post_id=post_id, created_at=datetime.utcnow())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()

def create_business(db: Session, business: schemas.BusinessCreate) -> models.Business:
    db_business = models.Business(**business.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_businesses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Business).offset(skip).limit(limit).all()

def create_location(db: Session, location: schemas.LocationCreate) -> models.Location:
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.MessageCreate, sender_id: int, receiver_id: int) -> models.Message:
    msg = models.Message(**message.dict(), sender_id=sender_id, receiver_id=receiver_id, created_at=datetime.utcnow())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    sender = get_user(db, sender_id)
    create_notification(db, receiver_id, "message", f"New message from {sender.username}")
    return msg

def create_group(db: Session, group: schemas.GroupCreate) -> models.Group:
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def get_group(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()

def create_notification(db: Session, user_id: int, ntype: str, content: str):
    note = models.Notification(user_id=user_id, type=ntype, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).offset(skip).limit(limit).all()

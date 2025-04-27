from backend.common.database import SessionLocal
from backend.social.app import crud, schemas

def seed():
    db = SessionLocal()
    try:
        if not crud.get_user(db, 1):
            # Create demo user with a VENDOR role
            crud.create_user(db, schemas.UserCreate(
                username="demo", email="demo@boatable.io", password="demo", roles=["VENDOR"]
            ))
            # Create a second sample user with a MECHANIC role if not already present
            if not crud.get_user_by_username(db, "alice"):
                crud.create_user(db, schemas.UserCreate(
                    username="alice", email="alice@example.com", password="alice123", roles=["MECHANIC"]
                ))
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()

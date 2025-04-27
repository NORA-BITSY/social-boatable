from sqlalchemy import event
from sqlalchemy.orm import Session
from backend.common.graph import record_follow

def after_flush(session: Session, flush_context, _):
    for instance in session.new:
        if instance.__class__.__name__ == "UserFollow":
            record_follow(instance.follower_id, instance.followee_id)

event.listen(Session, "after_flush", after_flush, propagate=True)

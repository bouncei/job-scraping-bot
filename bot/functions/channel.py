from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.channel import Channel
from . import db

def create_channel(user_id: str, channel_id: str) -> str:
    if check_channel(user_id, channel_id):
        return f"Channel '{channel_id}' already exists"

    channel = Channel(user_id=user_id, channel_id=channel_id)
    db.add(channel)

    try:
        db.commit()
        return f"Channel '{channel_id}' added successfully"
    except IntegrityError:
        db.rollback()
        return f"Channel '{channel_id}' already exists"
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemy error: {e}")
        return "Failed to add channel due to a database error."
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return "Failed to add channel due to an unexpected error."

def get_channels(user_id: str):
    try:
        return db.query(Channel).filter_by(user_id=user_id).all()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_channel_by_id(id: str):
    try:
        return db.query(Channel).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_channel_by_channel_id(channel_id: str):
    try:
        return db.query(Channel).filter_by(channel=channel_id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def check_channel(user_id: str, channel_id: str):
    try:
        return db.query(Channel).filter_by(user_id=user_id, channel_id=channel_id).first() is not None
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def update_channel(old_channel_id: str, new_channel_id: str) -> str:
    channel = get_channel_by_channel_id(old_channel_id)
    if channel:
        if check_channel(channel.user_id, new_channel_id):
            return f"Channel '{new_channel_id}' already exists, try again."

        channel.channel_id = new_channel_id
        try:
            db.commit()
            return f"Channel updated to '{new_channel_id}'!"
        except IntegrityError:
            db.rollback()
            return f"Channel '{new_channel_id}' already exists"
        except SQLAlchemyError as e:
            db.rollback()
            print(f"SQLAlchemy error: {e}")
            return "Failed to update channel due to a database error."
        except Exception as e:
            db.rollback()
            print(f"Unexpected error: {e}")
            return "Failed to update channel due to an unexpected error."
    return "Channel not found"

def delete_channel(id: str) -> bool:
    try:
        channel = db.query(Channel).filter_by(id=id).first()
        if channel:
            db.delete(channel)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return False

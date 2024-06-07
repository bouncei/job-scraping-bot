from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.group import Group
from . import db


def add_group(user_id:str, group_id:str):
    if check_group(user_id, group_id):
        return f"Group Id '{group_id}' already exists"
    
    new_group = Group(user_id=user_id, group_id=group_id)
    db.add(new_group)

    try:
        db.commit()
        return f"Group Id '{group_id}' added successfully"
    except IntegrityError:
        db.rollback()
        return f"Group Id '{group_id}' already exists"
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemy error: {e}")
        return "Failed to add group due to a database error."
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return "Failed to add group due to an unexpected error."



def check_group(user_id:str, group_id:str):
    try:
        return db.query(Group).filter_by(user_id=user_id, group_id=group_id).first() is not None
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def get_groups(user_id:str):
    try:
        return db.query(Group).filter_by(user_id=user_id).all()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_group_by_id(id: str):
    try:
        return db.query(Group).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_group_by_group_id(group_id: str):
    try:
        return db.query(Group).filter_by(group_id=group_id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def delete_group(id: str):
    try:
        group = db.query(Group).filter_by(id=id).first()
        if group:
            db.delete(group)
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


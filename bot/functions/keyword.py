from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.keyword import Keyword
from . import db

def create_keyword(user_id: str, keyword_text: str) -> str:
    if check_keyword(user_id, keyword_text):
        return "Keyword already exists"

    keyword = Keyword(user_id=user_id, keyword=keyword_text)
    db.add(keyword)

    try:
        db.commit()
        return f"Keyword '{keyword_text}' added successfully"
    except IntegrityError:
        db.rollback()
        return "Keyword already exists"
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemy error: {e}")
        return "Failed to add keyword due to a database error."
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return "Failed to add keyword due to an unexpected error."

def get_keywords(user_id: str):
    try:
        return db.query(Keyword).filter_by(user_id=user_id).all()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_keyword_by_id(keyword_id: str):
    try:
        return db.query(Keyword).filter_by(id=keyword_id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_keyword_by_name(keyword_name: str):
    try:
        return db.query(Keyword).filter_by(keyword=keyword_name).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def check_keyword(user_id: str, keyword_text: str):
    try:
        return db.query(Keyword).filter_by(user_id=user_id, keyword=keyword_text).first() is not None
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def update_keyword(old_keyword_text: str, new_keyword_text: str) -> str:
    keyword = get_keyword_by_name(old_keyword_text)
    if keyword:
        if check_keyword(keyword.user_id, new_keyword_text):
            return f"Keyword '{new_keyword_text}' already exists, try again."

        keyword.keyword = new_keyword_text
        try:
            db.commit()
            return f"Keyword updated to '{new_keyword_text}'!"
        except IntegrityError:
            db.rollback()
            return "Keyword already exists"
        except SQLAlchemyError as e:
            db.rollback()
            print(f"SQLAlchemy error: {e}")
            return "Failed to update keyword due to a database error."
        except Exception as e:
            db.rollback()
            print(f"Unexpected error: {e}")
            return "Failed to update keyword due to an unexpected error."
    return "Keyword not found"

def delete_keyword(keyword_id: str) -> bool:
    try:
        keyword = db.query(Keyword).filter_by(id=keyword_id).first()
        if keyword:
            db.delete(keyword)
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

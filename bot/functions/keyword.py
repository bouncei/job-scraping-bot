from ..models.keyword import Keyword
from sqlalchemy.exc import IntegrityError
from . import db

def create_keyword(user_id: str, keyword_text: str) -> str:
    check = check_keyword(user_id, keyword_text)

    if check:
        return "Keyword already exists" 

    keyword = Keyword(user_id, keyword=keyword_text)
    db.add(keyword)

    try: 
        db.commit()
        return "Keyword added successfully"
    except IntegrityError:
        db.rollback()
        return "Keyword already exists" 
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return False
        

def get_keywords(user_id):
    return db.query(Keyword).filter_by(user_id=user_id).all()

def check_keyword(user_id, keyword_text):
    keyword = db.query(Keyword).filter_by(user_id=user_id, keyword=keyword_text).first()

    if keyword is None:
        return False

    return keyword


def update_keyword(keyword_id, new_keyword_text):
    keyword = db.query(Keyword).filter_by(id=keyword_id).first()
    if keyword:
        keyword.keyword = new_keyword_text
        db.commit()
        return keyword
    return None

def delete_keyword(keyword_id):
    keyword = db.query(Keyword).filter_by(id=keyword_id).first()
    if keyword:
        db.delete(keyword)
        db.commit()
        return True
    return False


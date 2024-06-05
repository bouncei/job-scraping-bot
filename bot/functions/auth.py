from ..models.user import User
from .. import engine
from sqlalchemy.exc import IntegrityError
import bcrypt
from . import db



def register_user(username: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password.decode('utf-8'))
    db.add(user)

    try:
        db.commit()
        return True  # Registration successful
    except IntegrityError:
        db.rollback()
        return False  # Username already exists


def authenticate_user(username: str, password: str) -> bool | object:
    user = db.query(User).filter_by(username=username).first()

    if user is None:
        return False
    
    hashed_password = user.password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return user # Auth successful
    else:
        return False # Incorrect password
    

def login_user(user_id: int):
    session['user_id'] = user_id

def logout_user():
    session.pop('user_id', None)

def get_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        db = SessionLocal()
        user = db.query(User).get(user_id)
        db.close()
        return user
    return None

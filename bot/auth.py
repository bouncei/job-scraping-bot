from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from .models.user import User
from . import engine
from sqlalchemy.exc import IntegrityError
import bcrypt


Session = sessionmaker(bind=engine)
session = Session()

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password.decode('utf-8'))
    session.add(user)

    try:
        session.commit()
        return True  # Registration successful
    except IntegrityError:
        session.rollback()
        return False  # Username already exists


def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username).first()

    if user is None:
        return False
    
    hashed_password = user.password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return user # Auth successful
    else:
        return False # Incorrect password
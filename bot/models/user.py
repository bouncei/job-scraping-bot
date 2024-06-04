from sqlalchemy import Column, Integer, String
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(username='{self.username}'')>"

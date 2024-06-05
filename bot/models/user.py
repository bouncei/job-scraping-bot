from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    # Define the relationship to the Job and Keyword models
    # jobs = relationship('Job', back_populates='user')
    # keywords = relationship('Keyword', back_populates='user')


    def __repr__(self):
        return f"<User(username='{self.username}'')>"

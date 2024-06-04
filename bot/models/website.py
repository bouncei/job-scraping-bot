from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='websites')
    name = Column(String)
    url = Column(String, unique=True)

    def __repr__(self):
        return f"<Website(name='{self.name}', url='{self.url}')>"
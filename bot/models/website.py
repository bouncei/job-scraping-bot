from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from . import Base

class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    url = Column(String, unique=True)

    def __repr__(self):
        return f"<Website(url='{self.url}')>"
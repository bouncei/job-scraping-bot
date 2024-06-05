from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    keyword = Column(String, unique=True)

    def __repr__(self):
        return f"<Keyword(keyword='{self.keyword}')>"
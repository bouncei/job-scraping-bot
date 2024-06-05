from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    keyword = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Keyword(keyword='{self.keyword}')>"
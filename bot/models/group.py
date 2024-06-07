from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from . import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger,  nullable=False)
    group_id=Column(String, nullable=False)
    

    def __repr__(self):
        return f"<Group(title='{self.group_id}'')>"
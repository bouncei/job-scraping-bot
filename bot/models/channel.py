from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from . import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger,  nullable=False)
    channel_id=Column(String, nullable=False)
    

    def __repr__(self):
        return f"<Channel(channel_id='{self.channel_id}'')>"
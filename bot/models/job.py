from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    # user = relationship('User', back_populates='jobs')
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    source = Column(String)
    posted_at = Column(DateTime)


    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}', location='{self.location}')>"
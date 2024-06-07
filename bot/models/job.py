from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger,  nullable=False)
    # user = relationship('User', back_populates='jobs')
    title = Column(String,  nullable=False)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    status=Column(String, default="none") #Options: applied, declined
    source = Column(String, unique=True,  nullable=False)
    posted_at = Column(DateTime,  nullable=False)


    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}', location='{self.location}, status='{self.status}')>"
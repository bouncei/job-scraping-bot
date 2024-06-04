# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from . import Base

# class Resume(Base):
#     __tablename__ = 'resumes'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='resumes')
#     content = Column(Text)

#     def __repr__(self):
#         return f"<Resume(user_id='{self.user_id}')>"
from sqlalchemy.orm import sessionmaker
from .. import engine

Session = sessionmaker(bind=engine)
db = Session()
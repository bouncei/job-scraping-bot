from sqlalchemy import create_engine
from ..main import db_url
from .models import Base

# Create the engine
engine = create_engine(db_url)


# Create the database tables
Base.metadata.create_all(engine)

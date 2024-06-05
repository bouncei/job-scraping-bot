from sqlalchemy import create_engine
from .models import Base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

# Define the database URL
db_url = os.getenv("DB_URL")


if db_url is None:
    raise ValueError("No DB_URL found in environment variables")

# Create the engine
engine = create_engine(db_url)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models to create tables
# from .models.user import User
from .models.job import Job
from .models.keyword import Keyword
# from .models.resume import Resume

# Create the database tables
Base.metadata.create_all(engine)

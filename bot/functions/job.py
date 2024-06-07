from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.job import Job
from . import db


def create_job(user_id: str, company: str, location: str, description: str, source: str, posted_at: str):
    if check_job(user_id, source):
        return f"Job with url '{source} already exists"
    
    new_job = Job(user_id=user_id, company=company, location=location, description=description, source=source, posted_at=posted_at)
    db.add(new_job)

    try:
        db.commit()
        return f"New job added succcessfully"
    except IntegrityError:
        db.rollback()
        return f"Job with url '{source}' already exists"
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return "Failed to add job due to an unexpected error."
    


def check_job(user_id: str, source: str):
    try:
        return db.query(Job).filter_by(user_id=user_id, source=source).first() is not None
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False




def get_jobs(user_id:str):
    """
    Get jobs, filtered by a user id
    """
    try:
        return db.query(Job).filter_by(user_id=user_id).all()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def get_job_by_id(job_id: str):
    """
    Get job by it's unique id
    """
    try:
        return db.query(Job).filter_by(id=job_id).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_job_by_source(job_source: str):
    """
    Get job by it's unique source
    """
    try:
        return db.query(Job).filter_by(source=job_source).first()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def update_job_status(job_source:str, status: str) -> str:
    """
    Update a job's status (Options: none, applied, declined)
    """
    job = get_job_by_source(job_source)

    if job:
        if job.source == status:
            return f"Job already has a status of '{status}'"
        
        job.status = status
        try:
            db.commit()
            return f"Job status updated to '{status}'"

        except IntegrityError:
            db.rollback()
            return f"Job already has a status of '{status}'"
        except SQLAlchemyError as e:
            db.rollback()
            print(f"SQLAlchemy error: {e}")
            return "Failed to update job due to a database error."
        except Exception as e:
            db.rollback()
            print(f"Unexpected error: {e}")
            return "Failed to update job due to an unexpected error."
    return "Job not found"

def delete_job(job_source:str)-> bool:
    """
    Delete a user's saved job
    """
    try:
        job = get_job_by_source(job_source)

        if job:
            db.delete(job)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"SQLAlchemy error: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return False
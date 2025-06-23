from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, DisconnectionError
from models.database import WindowCalculation
from database.config import engine
from typing import List
import time
import logging

def retry_db_operation(max_retries=3, delay=1, backoff=2):
    """Decorator to retry database operations with exponential backoff"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DisconnectionError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logging.error(f"Database operation failed after {max_retries} retries: {str(e)}")
                        raise
                    
                    wait_time = delay * (backoff ** (retries - 1))
                    logging.warning(f"Database connection failed, retrying in {wait_time}s... (attempt {retries}/{max_retries})")
                    time.sleep(wait_time)
                except Exception as e:
                    # Don't retry non-connection errors
                    logging.error(f"Non-connection database error: {str(e)}")
                    raise
            return None
        return wrapper
    return decorator

class DatabaseService:
    
    @staticmethod
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def create_calculation(calculation_data: dict) -> WindowCalculation:
        """Create a new window calculation record"""
        calculation = WindowCalculation(**calculation_data)
        
        with Session(engine) as db_session:
            db_session.add(calculation)
            db_session.commit()
            db_session.refresh(calculation)
            return calculation
    
    @staticmethod
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def get_all_calculations() -> List[WindowCalculation]:
        """Get all calculations ordered by creation date"""
        with Session(engine) as session:
            statement = select(WindowCalculation)
            return list(session.exec(statement).all())
    
    @staticmethod
    @retry_db_operation(max_retries=3, delay=1, backoff=2)
    def delete_calculation(calculation_id: int) -> bool:
        """Delete a calculation"""
        with Session(engine) as session:
            calculation = session.get(WindowCalculation, calculation_id)
            if calculation:
                session.delete(calculation)
                session.commit()
                return True
            return False
from sqlmodel import Session, select
from models.database import WindowCalculation
from database.config import engine
from typing import List

class DatabaseService:
    
    @staticmethod
    def create_calculation(calculation_data: dict) -> WindowCalculation:
        """Create a new window calculation record"""
        calculation = WindowCalculation(**calculation_data)
        
        with Session(engine) as db_session:
            db_session.add(calculation)
            db_session.commit()
            db_session.refresh(calculation)
            return calculation
    
    @staticmethod
    def get_all_calculations() -> List[WindowCalculation]:
        """Get all calculations ordered by creation date"""
        with Session(engine) as session:
            statement = select(WindowCalculation)
            return list(session.exec(statement).all())
    
    @staticmethod
    def delete_calculation(calculation_id: int) -> bool:
        """Delete a calculation"""
        with Session(engine) as session:
            calculation = session.get(WindowCalculation, calculation_id)
            if calculation:
                session.delete(calculation)
                session.commit()
                return True
            return False
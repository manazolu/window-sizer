from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class WindowCalculation(SQLModel, table=True):
    __tablename__ = "window_calculations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    selected_width: int
    selected_height: int
    frame_type: str  # Use string directly to match database enum
    color: str = Field(max_length=50)
    calculated_width: int
    calculated_height: int
    wing_size: int
    rope_length: int
    net_size: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
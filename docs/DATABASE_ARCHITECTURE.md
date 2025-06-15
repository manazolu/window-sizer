# Database Architecture Document
## Window Sizer Application - PostgreSQL Integration

### Executive Summary

This document outlines the simplified database architecture for the Window Sizer application. The database structure has been streamlined to focus on core window calculation functionality with a single table approach.

### Current State Analysis

**Existing Data Flow:**
```
User Input → Calculations → In-Memory Table → PDF Generation
```

**Current Limitations:**
- Data lost when application restarts
- No historical tracking of calculations
- No audit trail or analytics capability
- Single-session data only

### Simplified Architecture

#### Database Integration Strategy

**New Data Flow:**
```
User Input → Calculations → Database Storage → Table Display → PDF Generation
                     ↓
            Historical Data & Analytics
```

### Database Schema Design

#### Simplified Single-Table Structure

The database structure has been simplified to use a single table approach, removing the complexity of customer relationships and sessions for the initial implementation:

```sql
-- Create enum for frame types
CREATE TYPE frame_type_enum AS ENUM ('18mm', '18mm-flis', '25mm', '26mm');

-- Window calculations table (simplified)
CREATE TABLE window_calculations (
    id SERIAL PRIMARY KEY,
    selected_width INTEGER NOT NULL,
    selected_height INTEGER NOT NULL,
    frame_type frame_type_enum NOT NULL,
    color VARCHAR(50) NOT NULL,
    calculated_width INTEGER NOT NULL,
    calculated_height INTEGER NOT NULL,
    wing_size INTEGER NOT NULL,
    rope_length INTEGER NOT NULL,
    net_size DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Key Simplifications

1. **Removed Customer Table**: Eliminated customer relationship complexity
2. **Removed Sessions**: No session grouping for now
3. **Single Entity**: All calculation data in one table
4. **Essential Fields Only**: Focus on core calculation data
5. **Type Safety**: Uses PostgreSQL enum for frame types

#### Performance Optimizations

```sql
-- Index for performance on date queries
CREATE INDEX idx_window_calculations_created_at ON window_calculations(created_at);
```

### Environment Setup (Completed ✅)

#### Docker PostgreSQL Configuration
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15-alpine
    container_name: window-sizer-db
    environment:
      POSTGRES_DB: window_sizer
      POSTGRES_USER: window_user
      POSTGRES_PASSWORD: window_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U window_user -d window_sizer"]
      interval: 10s
      timeout: 5s
      retries: 5
```

#### Dependencies
```toml
[project]
dependencies = [
    # ... existing dependencies
    "sqlmodel>=0.0.24",
    "psycopg2-binary>=2.9.10",
    "alembic>=1.16.1",
    "python-dotenv>=1.0.0",
]
```

### SQLModel Implementation Plan

#### 1. Simplified Database Model

```python
# models/database.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class FrameType(str, Enum):
    MM_18 = "18mm"
    MM_18_FLIS = "18mm-flis" 
    MM_25 = "25mm"
    MM_26 = "26mm"

class WindowCalculation(SQLModel, table=True):
    __tablename__ = "window_calculations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    selected_width: int
    selected_height: int
    frame_type: FrameType
    color: str = Field(max_length=50)
    calculated_width: int
    calculated_height: int
    wing_size: int
    rope_length: int
    net_size: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### 2. Database Configuration

```python
# database/config.py
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://window_user:window_pass@localhost:5432/window_sizer"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session
```

#### 3. Simplified Database Service

```python
# services/database_service.py
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
            statement = select(WindowCalculation).order_by(
                WindowCalculation.created_at.desc()
            )
            return session.exec(statement).all()
    
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
```

### Implementation Phases

#### Phase 1: Environment Setup ✅ (Completed)
- [x] Docker Compose PostgreSQL configuration
- [x] Environment variables setup (.env)
- [x] Simplified database initialization script (init.sql)
- [x] Dependencies installation (SQLModel, psycopg2, etc.)
- [x] Database container running and verified

#### Phase 2: Database Models (Next)
- [ ] Create simplified SQLModel model
- [ ] Set up database connection configuration
- [ ] Create basic database service layer
- [ ] Test database connectivity from Python

#### Phase 3: Application Integration (Future)
- [ ] Modify `add_to_table()` to save to database
- [ ] Update table display to load from database
- [ ] Add delete functionality with database sync
- [ ] Update PDF generation to use database data

#### Phase 4: Enhanced Features (Future)
- [ ] Search and filter capabilities
- [ ] Historical data viewing
- [ ] Export/import functionality
- [ ] Data analytics dashboard

### Current Status

✅ **Completed:**
- Docker PostgreSQL container setup
- Simplified database schema with single table:
  - `window_calculations` (with enum frame types)
- Environment configuration
- Dependencies installed
- Sample data for testing

🔄 **Next Steps:**
1. Create simplified SQLModel model matching database schema
2. Set up database connection in application
3. Create basic CRUD operations
4. Test database integration

### Database Commands Reference

```bash
# Start database
docker-compose up -d postgres

# Stop database
docker-compose down

# View logs
docker-compose logs postgres

# Connect to database
docker exec window-sizer-db psql -U window_user -d window_sizer

# Check tables
docker exec window-sizer-db psql -U window_user -d window_sizer -c "\dt"

# Query data
docker exec window-sizer-db psql -U window_user -d window_sizer -c "SELECT * FROM window_calculations;"
```

### Benefits of Simplified Approach

1. **Reduced Complexity**: Single table eliminates joins and relationship management
2. **Faster Implementation**: Less code to write and maintain
3. **Better Performance**: No complex queries or foreign key constraints
4. **Easier Migration**: Simpler data structure for future enhancements
5. **Development Speed**: Rapid prototyping and testing capabilities

### Future Expansion Possibilities

When additional complexity is needed, the simplified structure can be enhanced with:
- Customer relationship tables
- Session grouping functionality
- Advanced analytics and reporting
- User management and authentication
- Multi-tenant support

---

**Document Version**: 2.0  
**Created**: 2025-06-15  
**Updated**: 2025-06-15 (Simplified Architecture)  
**Author**: Architecture Review  
**Status**: Phase 1 Complete - Simplified Single-Table Design
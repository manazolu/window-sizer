-- Window Sizer Database Initialization Script
-- This script runs automatically when PostgreSQL container starts

-- Create enum for frame types
CREATE TYPE frame_type_enum AS ENUM ('18mm', '18mm-flis', '25mm', '26mm');

-- Window calculations table
CREATE TABLE IF NOT EXISTS window_calculations (
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
-- Create indexes for performance

CREATE INDEX IF NOT EXISTS idx_window_calculations_created_at ON window_calculations(created_at);

-- Insert sample data for testing (optional)
INSERT INTO window_calculations (selected_width, selected_height, frame_type, color, calculated_width, calculated_height, wing_size, rope_length, net_size) VALUES 
    (100, 200, '18mm', 'White', 120, 220, 10, 15, 50.00),
    (150, 250, '25mm', 'Black', 170, 270, 12, 20, 75.00)
ON CONFLICT DO NOTHING;

-- Grant permissions to application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO window_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO window_user;
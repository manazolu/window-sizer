# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Development:**
- `uv sync` - Install/sync dependencies
- `uv run main.py` - Run the application locally (serves on 0.0.0.0)

**Dependencies:**
- Uses `uv` for Python package management (requires Python >=3.13)
- System packages required for WeasyPrint PDF generation: `libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`

## Architecture

This is a single-file NiceGUI web application (`main.py`) that calculates window dimensions based on frame types and generates PDF reports.

**Core Components:**
- **UI Layer**: NiceGUI-based web interface with input fields, table display, and action buttons
- **Calculation Engine**: Functions for computing window dimensions based on frame type (18mm, 25mm, 26mm, 18mm-flis)
- **PDF Generation**: WeasyPrint + Jinja2 templating system using `templates/pdf_template.html`

**Key Calculations:**
- Width/height adjustments vary by frame type (RAM)
- Wing calculations depend on frame type
- Rope calculation: `(width + height) * 2`  
- Net calculation varies by frame type (divide by 2 or 3)

**Data Flow:**
1. User inputs dimensions, selects frame type and color
2. Calculations performed via dedicated functions
3. Results added to in-memory table
4. PDF generated from table data using HTML template
5. PDF downloaded via browser

**Template System:**
- `templates/pdf_template.html` - A4 landscape PDF template with company branding
- Uses Jinja2 for dynamic content rendering
- Styled for professional appearance with header/footer

The application interface is in Croatian/Serbian language.
# Importing the module
from nicegui import ui, app
from nicegui.elements.label import Label
from weasyprint import HTML  # type: ignore
from jinja2 import Environment, FileSystemLoader
import datetime
import tempfile
import os
from calculations import (
    calculate_new_width,
    calculate_new_height,
    calculate_wing,
    calculate_rope,
    calculate_net
)
from config import TABLE_COLUMNS, FRAME_OPTIONS, COLOR_OPTIONS
from services.database_service import DatabaseService

customer_name= ''
        
def add_to_table(selected_width: int, selected_height: int, frame: str, color: str):
    try:
        new_height = calculate_new_height(selected_height, frame)
        new_width = calculate_new_width(selected_width, frame)
        wing_size = calculate_wing(new_height, frame)
        rope_length = calculate_rope(selected_width, selected_height)
        net_size = calculate_net(selected_width, frame)
        
        # Save to database
        calculation_data = {
            'selected_width': selected_width,
            'selected_height': selected_height,
            'frame_type': frame,
            'color': color,
            'calculated_width': new_width,
            'calculated_height': new_height,
            'wing_size': wing_size,
            'rope_length': rope_length,
            'net_size': float(net_size),
        }
        
        try:
            db_record = DatabaseService.create_calculation(calculation_data)
            # Add to UI table with database ID
            table.add_row({
                'id': db_record.id,  # Use database ID
                'selected_width': selected_width,
                'selected_height': selected_height,
                'frame': frame,
                'color': color,
                'calculated_width': new_width,
                'calculated_height': new_height,
                'wing': wing_size,
                'rope': rope_length,
                'net': net_size,
            })
            ui.notify("Uspješno dodano!", color='green')
        except Exception as db_error:
            ui.notify(f"Greška pri spremanju u bazu: {str(db_error)}", color='red')
        
    except ValueError as e:
        ui.notify(f"Napaka: {str(e)}", color='red')

def generate_pdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('pdf_template.html')

    html_out = template.render(
        columns=TABLE_COLUMNS,
        rows=table.rows,
        customer_name=customer_name,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    return HTML(string=html_out).write_pdf()

def generate_and_open_pdf():
    if not table.rows:
        ui.notify('Tabela je prazna, dodaj redove prije generiranja PDF-a.')
        return
    
    try:
        pdf_bytes = generate_pdf()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        # Serve the file and open in new tab
        pdf_url = f'/pdf/{os.path.basename(tmp_path)}'
        app.add_static_file(local_file=tmp_path, url_path=pdf_url)
        ui.run_javascript(f'window.open("{pdf_url}", "_blank");')
        
    except Exception as e:
        ui.notify(f'Greška pri generiranju PDF-a: {str(e)}', color='red')
        return
    
def generate_and_save_pdf():
    if not table.rows:
        ui.notify('Tabela je prazna, dodaj redove prije generiranja PDF-a.')
        return
    
    try:
        pdf_bytes = generate_pdf()
        ui.download(pdf_bytes, 'izracun.pdf', 'application/pdf')

    except Exception as e:
        ui.notify(f'Greška pri generiranju PDF-a: {str(e)}', color='red')
        return
    
def update_customer_name(value):
    global customer_name
    customer_name = value

def load_calculations_from_database():
    """Load existing calculations from database into the UI table"""
    try:
        calculations = DatabaseService.get_all_calculations()
        for calc in calculations:
            table.add_row({
                'id': calc.id,
                'selected_width': calc.selected_width,
                'selected_height': calc.selected_height,
                'frame': calc.frame_type,
                'color': calc.color,
                'calculated_width': calc.calculated_width,
                'calculated_height': calc.calculated_height,
                'wing': calc.wing_size,
                'rope': calc.rope_length,
                'net': calc.net_size,
            })
        if calculations:
            ui.notify(f"Učitano {len(calculations)} zapisa iz baze", color='blue')
    except Exception as e:
        ui.notify(f"Greška pri učitavanju iz baze: {str(e)}", color='orange')

def delete_selected_rows():
    """Delete selected rows from both UI table and database"""
    if not table.selected:
        return
    
    try:
        # Delete from database first
        deleted_count = 0
        for row in table.selected:
            row_id = row['id']
            if DatabaseService.delete_calculation(row_id):
                deleted_count += 1
        
        # Remove from UI table
        table.remove_rows(table.selected)
        
        if deleted_count > 0:
            ui.notify(f"Obrisano {deleted_count} zapisa", color='green')
        else:
            ui.notify("Greška pri brisanju iz baze", color='red')
            
    except Exception as e:
        ui.notify(f"Greška pri brisanju: {str(e)}", color='red')


with ui.row():
    selected_width = ui.input(label='Sirina [mm]', placeholder='Unesi sirinu',
        validation={'Unesi milimetre za sirinu': lambda value: value.isdigit() and int(value) > 0},
    )

    selected_height = ui.input(label='Visina [mm]', placeholder='Unesi visinu',
        validation={'Unesi milimetre za visinu': lambda value: value.isdigit() and int(value) > 0},
    )

    selected_frame = ui.select(label='Ram', options=FRAME_OPTIONS, value='18mm')

    selected_color = ui.select(label='Boja', options=COLOR_OPTIONS, value='Bjela')

    ui.button('Dodaj', on_click=lambda: add_to_table(selected_width.value, selected_height.value, selected_frame.value, selected_color.value))


table = ui.table(columns=TABLE_COLUMNS, rows=[], selection='multiple')

# Load existing data from database
load_calculations_from_database()

with ui.row():
    ui.button('Izbrisi', on_click=delete_selected_rows, color='red') \
        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))
with ui.row():
    ui.input(label='Unesite ime stranke', placeholder='', on_change=lambda e: update_customer_name(e.value))
    with ui.dropdown_button('Print PDF', icon='print', split=True, on_click=lambda: generate_and_open_pdf()):
        ui.button('Sacuvaj PDF', icon='save', on_click=lambda: generate_and_save_pdf()).classes('w-full')

ui.run(host='0.0.0.0', title='Prozori')
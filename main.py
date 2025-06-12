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
        
def add_to_table(selected_width: int, selected_height: int, frame: str, color: str):
    try:
        new_height = calculate_new_height(selected_height, frame)
        table.add_row({
            'id': len(table.rows),  # Unique ID for the row
            'selected_width': selected_width,
            'selected_height': selected_height,
            'frame': frame,
            'color': color,
            'calculated_width': calculate_new_width(selected_width, frame),
            'calculated_height': new_height,
            'wing': calculate_wing(new_height, frame),
            'rope': calculate_rope(selected_width, selected_height),
            'net': calculate_net(selected_width, frame),
        })
    except ValueError as e:
        ui.notify(f"Napaka: {str(e)}", color='red')

def generate_pdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('pdf_template.html')

    html_out = template.render(
        columns=TABLE_COLUMNS,
        rows=table.rows,
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
with ui.row():
    ui.button('Izbrisi', on_click=lambda: table.remove_rows(table.selected), color='red') \
        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))
    ui.button('Natisni PDF', on_click=lambda: generate_and_open_pdf()) \

ui.run(host='0.0.0.0', title='Prozori')
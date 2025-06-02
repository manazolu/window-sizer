# Importing the module 
from nicegui import ui
from nicegui.elements.label import Label
from weasyprint import HTML  # type: ignore
from jinja2 import Environment, FileSystemLoader
import datetime

def delete_row(row_index):
    table.remove_rows(table.rows[row_index])       

def delete_all_rows():
    table.rows.clear()
    table.update()

def calculate_new_width(width, ram):
    if ram == '18mm':
        return (int(width) - 30)
    elif ram == '25mm':
        return (int(width) - 24)
    elif ram == '26mm':
        return (int(width) - 40)
    elif ram == '18mm-flis':
        return (int(width) - 62)
    else:
        raise ValueError("Invalid ram value")
    
def calculate_new_height(height, ram):
    if ram == '18mm':
        return (int(height) - 50)
    elif ram == '25mm':
        return (int(height) - 55)
    elif ram == '26mm':
        return (int(height) - 77)
    elif ram == '18mm-flis':
        return (int(height) - 62)
    else:
        raise ValueError("Invalid ram value")

def calculate_wing(new_height, ram):
    if ram == '18mm-flis':
        return (int(new_height) - 11)
    else:
        return (int(new_height) - 7)

def calculate_rope(width, height):
    return((int(width) + int(height) * 2))

def calculate_net(width, ram):
    if ram == '18mm' or ram == '18mm-flis':
        return (int(width) / 2)
    elif ram == '25mm' or ram == '26mm':
        return (int(width) / 3)
    else:
        raise ValueError("Invalid ram value")
        
def add_to_table(selected_width: int, selected_height: int, ram: str, color: str):
    try:
        new_height = calculate_new_height(selected_height, ram)
        table.add_row({
            'selected_width': selected_width,
            'selected_height': selected_height,
            'ram': ram,
            'color': color,
            'calculated_width': calculate_new_width(selected_width, ram),
            'calculated_height': new_height,
            'wing': calculate_wing(new_height, ram),
            'rope': calculate_rope(selected_width, selected_height),
            'net': calculate_net(selected_width, ram),
        })
    except ValueError as e:
        ui.notify(f"Napaka: {str(e)}", color='red')

def generate_pdf():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('pdf_template.html')

    html_out = template.render(
        columns=columns,
        rows=table.rows,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    return HTML(string=html_out).write_pdf()

def generate_and_download_pdf():
    if not table.rows:
        ui.notify('Tabela je prazna, dodaj redove prije generiranja PDF-a.')
        return
    
    try:
        pdf_bytes = generate_pdf()
        ui.download(pdf_bytes, 'izracun.pdf', 'application/pdf')
    except Exception as e:
        ui.notify(f'Greška pri generiranju PDF-a: {str(e)}', color='red')
        return


columns = [
    {'name': 'selected_width', 'label': 'Sirina', 'field': 'selected_width', 'required': True, 'align': 'left'},
    {'name': 'selected_height', 'label': 'Visina', 'field': 'selected_height', 'required': True, 'align': 'left'},
    {'name': 'ram', 'label': 'RAM', 'field': 'ram', 'required': True, 'align': 'left'},
    {'name': 'color', 'label': 'Boja', 'field': 'color', 'required': True, 'align': 'left'},
    {'name': 'calculated_width', 'label': 'Izracunana Sirina', 'field': 'calculated_width', 'required': True, 'align': 'left'},
    {'name': 'calculated_height', 'label': 'Izracunana Visina', 'field': 'calculated_height', 'required': True, 'align': 'left'},
    {'name': 'wing', 'label': 'Krilo', 'field': 'wing', 'required': True, 'align': 'left'},
    {'name': 'rope', 'label': 'Spaga', 'field': 'rope', 'required': True, 'align': 'left'},
    {'name': 'net', 'label': 'Mrezica', 'field': 'net', 'required': True, 'align': 'left'},
]


with ui.row():
    selected_width = ui.input(label='Sirina [mm]', placeholder='Unesi sirinu',
        validation={'Unesi milimetre za sirinu': lambda value: value.isdigit() and int(value) > 0},
    )

    selected_height = ui.input(label='Visina [mm]', placeholder='Unesi visinu',
        validation={'Unesi milimetre za visinu': lambda value: value.isdigit() and int(value) > 0},
    )

    selected_ram = ui.select(label='RAM', options=['18mm', '18mm-flis', '25mm', '26mm'], value='18mm')

    selected_color = ui.select(label='Boja', options=['Bjela', 'Smedja', 'Antracit', 'Siva', 'Zlatni hrast'], value='Bjela')

    ui.button('Dodaj', on_click=lambda: add_to_table(selected_width.value, selected_height.value, selected_ram.value, selected_color.value))


table = ui.table(columns=columns, rows=[], row_key='name')
with ui.row():
    ui.button('Izbrisi sve', on_click=lambda: delete_all_rows(), color='red')
    ui.button('Natisni PDF', on_click=lambda: generate_and_download_pdf())

ui.run(host='0.0.0.0', title='Prozori')
# Importing the module 
from nicegui import ui
from nicegui.elements.label import Label
        

def calculate_new_width(width, ram):
    if ram == '18mm':
        return (int(width) - 30)
    elif ram == '25mm':
        return (int(width) - 24)
    elif ram == '26mm':
        return (int(width) - 40)
    else:
        raise ValueError("Invalid ram value")
    
def calculate_new_height(height, ram):
    if ram == '18mm':
        return (int(height) - 50)
    if ram == '25mm':
        return (int(height) - 55)
    if ram == '26mm':
        return (int(height) - 77)
    else:
        raise ValueError("Invalid ram value")

def calculate_wing(new_height):
    return (int(new_height) - 7)

def calculate_rope(width, height):
    return((int(width) + int(height) * 2))

def calculate_net(width, ram):
    if ram == '18mm':
        return (int(width) / 2)
    elif ram == '25mm' or ram == '26mm':
        return (int(width) / 3)
    else:
        raise ValueError("Invalid ram value")
        
def add_to_table(selected_width: int, selected_height: int, ram: str):
    new_width = calculate_new_width(selected_width, ram)
    new_height = calculate_new_height(selected_height, ram)
    wing = calculate_wing(new_height)
    rope = calculate_rope(selected_width, selected_height)
    net = calculate_net(selected_width, ram)
    table.add_row({
        'selected_width': selected_width, 
        'selected_height': selected_height, 
        'ram': ram, 
        'calculated_width': new_width,
        'calculated_height': new_height,
        'wing': wing,
        'rope': rope,
        'net': net
    })


columns = [
    {'name': 'selected_width', 'label': 'Sirina', 'field': 'selected_width', 'required': True, 'align': 'left'},
    {'name': 'selected_height', 'label': 'Visina', 'field': 'selected_height', 'required': True, 'align': 'left'},
    {'name': 'ram', 'label': 'RAM', 'field': 'ram', 'required': True, 'align': 'left'},
    {'name': 'calculated_width', 'label': 'Izracunana Sirina', 'field': 'calculated_width', 'required': True, 'align': 'left'},
    {'name': 'calculated_height', 'label': 'Izracunana Visina', 'field': 'calculated_height', 'required': True, 'align': 'left'},
    {'name': 'wing', 'label': 'Krilo', 'field': 'wing', 'required': True, 'align': 'left'},
    {'name': 'rope', 'label': 'Spaga', 'field': 'rope', 'required': True, 'align': 'left'},
    {'name': 'net', 'label': 'Mrezica', 'field': 'net', 'required': True, 'align': 'left'},
]


with ui.row():
    selected_width = ui.input(label='Sirina [mm]', placeholder='Unesi sirinu',
        validation={'Unesi milimetre za sirinu': lambda value: int(value) > 0},
    )

    selected_height = ui.input(label='Visina [mm]', placeholder='Unesi visinu',
        validation={'Unesi milimetre za sirinu': lambda value: int(value) > 0},
    )

    selected_ram = ui.select(label='RAM', options=['18mm', '25mm', '26mm'], value='18mm')

    ui.button('Izracunaj', on_click=lambda: add_to_table(selected_width.value, selected_height.value, selected_ram.value))


table = ui.table(columns=columns, rows=[], row_key='name')

ui.run()
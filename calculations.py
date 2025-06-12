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
    return((int(width) + int(height)) * 2)

def calculate_net(width, ram):
    if ram == '18mm' or ram == '18mm-flis':
        return (int(width) / 2)
    elif ram == '25mm' or ram == '26mm':
        return (int(width) / 3)
    else:
        raise ValueError("Invalid ram value")
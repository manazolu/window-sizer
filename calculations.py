def calculate_new_width(width, frame):
    if frame == '18mm':
        return (int(width) - 30)
    elif frame == '25mm':
        return (int(width) - 24)
    elif frame == '26mm':
        return (int(width) - 40)
    elif frame == '18mm-flis':
        return (int(width) - 62)
    else:
        raise ValueError("Invalid frame value")
    
def calculate_new_height(height, frame):
    if frame == '18mm':
        return (int(height) - 50)
    elif frame == '25mm':
        return (int(height) - 55)
    elif frame == '26mm':
        return (int(height) - 77)
    elif frame == '18mm-flis':
        return (int(height) - 62)
    else:
        raise ValueError("Invalid frame value")

def calculate_wing(new_height, frame):
    if frame == '18mm-flis':
        return (int(new_height) - 11)
    else:
        return (int(new_height) - 7)

def calculate_rope(width, height):
    return((int(width) + int(height)) * 2)

def calculate_net(width, frame):
    if frame == '18mm' or frame == '18mm-flis':
        return (int(width) / 2)
    elif frame == '25mm' or frame == '26mm':
        return (int(width) / 3)
    else:
        raise ValueError("Invalid frame value")
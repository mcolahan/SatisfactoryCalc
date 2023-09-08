
def get_display_of_number(val):
    if int(val) / val == 1:
        return str(int(val))
    elif len(str(val).split(".")[1]) > 3:
        return str(round(val, 3)) 
    else:
        return str(val)
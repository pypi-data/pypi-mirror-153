def INTput(prompt):
    try:
        x = int(input(prompt))
        return x
    except:
        raise ValueError("Input must be an integer")
def STRput(prompt):
    try:
        x = str(input(prompt))
        return x
    except:
        raise ValueError("Input must be a string")
def BOOLput(prompt):
    try:
        x = bool(input(prompt))
        return x
    except:
        raise ValueError("Input must be a boolean")

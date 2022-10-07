def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

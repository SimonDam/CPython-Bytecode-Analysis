def remove_end(line, end):
    return line.split(end)[0]

def csv_get_values(line, sep = ',', end = '\n'):
    line = remove_end(line, end)
    return tuple(line.split(sep)) # We don't return immediately to ensure that there are two values.

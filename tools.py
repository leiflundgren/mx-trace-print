import io

def read(file_thing) -> [str]:
    if isinstance(file_thing, io.TextIOBase):
        return file_thing.readlines()
    if isinstance(file_thing, str):
        if file_thing.count('\n') > 0:
            return file_thing # list-thing
        else:
            with open(file_thing, "r", encoding='iso-8859-1') as f:
                return f.readlines()
    raise ValueError("Cannot read data from " + str(type(file_thing)))

def open_file(name) -> io.TextIOBase:
    return open(name, "r", encoding='iso-8859-1')
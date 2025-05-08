def read(path: str):
    with open(path) as fd:
        return fd.read()

def read_as_binary(path: str):
    with open(path, 'rb') as fd:
        return fd.read()

def overwrite(path: str, content: str):
    with open(path, 'w') as fd:
        fd.write(content)

def add_line(path: str, content: str):
    with open(path, 'a') as fd:
        fd.write(f'\n{content}')

def clear(path: str):
    with open(path, 'w') as fd:
        fd.write('')

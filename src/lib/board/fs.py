def read(path):
    with open(path) as fd:
        return fd.read()

def overwrite(path, content):
    with open(path, 'w') as fd:
        fd.write(content)

def add_line(path, content):
    with open(path, 'a') as fd:
        fd.write(f'\n{content}')

def clear(path):
    with open(path, 'w') as fd:
        fd.write('')

from datetime import date
from os import remove
from os.path import exists

def writing_file(path, content, update=None):
    if update:
        if exists(path):
            remove(path)
    with open(path, 'a', encoding='utf-8') as file:
        file.write(content)
    return None

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
def date_today():
    return str(date.today())

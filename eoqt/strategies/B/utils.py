from pandas import Timestamp
from datetime import timedelta, date, datetime
from sys import path
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

def base_path():
    return path[0].replace('strategies\\B', '') # {% builder %}

def timed_out(time_ref, time_now):
    if time_now == str(Timestamp(time_ref) + timedelta(minutes=20))[11:]:
        return True
    return False

def try_sign(data):
    try:
        if data[0] == 'erro':
            pass
    except:
        data[0] = 0
    try:
        if data[1] == 'erro':
            pass
    except:
        data[1] = 0
    return data

def date_today():
    return str(date.today())

def day_week(date):
    date = datetime.strptime(date, '%Y-%m-%d').weekday()
    return ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'][date]

def timed_out(self, time_now):
    if time_now == str(Timestamp(self.open) + timedelta(minutes=20))[11:]:
        return True
    return False

def time():
    return datetime.today().strftime('%H:%M') + ':00'

def get_sign(_path_sign): # < check date sign >
    return read_file(_path_sign).split(', ')[3]

def dt():
    return datetime.today()

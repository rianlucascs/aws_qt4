from sys import path
from control.log import LogQt
class Data:

    @staticmethod
    def read():
        _path = f'{path[0]}\\Control\\settings.txt'
        with open(_path, 'r', encoding='utf-8') as file:
            file = file.read().split(', ')
        LogQt('Data read').startup
        return file
        
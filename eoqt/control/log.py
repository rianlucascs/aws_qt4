
from sys import path
from datetime import datetime
from control.utils import writing_file

class LogQt:

    def __init__(self, base):
        self._path = f'{path[0]}\\logs\\executionHistory.txt' 
        self.base = base
    
    def dt(self):
        return datetime.today()
        
    @property
    def startup(self):
        content = f'[ {self.dt()} ] Control\{self.base}\n'
        return writing_file(self._path, content)

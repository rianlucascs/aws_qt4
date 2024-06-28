

from acess import Acess
from utils import writing_file, dt

class LogQT():

    def __init__(self, base):
        self.base = base
        self._path = Acess()._path
        self._name = Acess()._name
    
    @property
    def startup(self):
        content = f'[ {dt()} ] {self._name}\{self.base}\n'
        path = self._path.replace(f'\\strategies\\{self._name}', '')
        new_path = f'{path}\\logs\\Execution{self._name}_History.txt'
        return writing_file(new_path, content)
    

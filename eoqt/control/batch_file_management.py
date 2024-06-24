
from os import startfile, remove
from os.path import exists
from control.log import LogQt
from time import sleep

class BatchFileManagement:
    
    def __init__(self, path_strat, filename):
        self.filename = filename
        self._path_strat = path_strat
        self._path_bat = f'{path_strat}\\{filename}.bat'

    def _create(self):
        if exists(self._path_bat):
            remove(self._path_bat)
            LogQt(f'BatchFileManagement remove {self._path_strat[-1]}').startup
        sleep(2)
        with open(self._path_bat, 'a', encoding='utf-8') as file:
            file.write(f'cd {self._path_strat}\npython {self.filename}.py')
            LogQt(f'BatchFileManagement create {self._path_strat[-1]}').startup
        sleep(2)
        return None
    
    def start(self):
        self._create()
        startfile(self._path_bat)
        LogQt(f'BatchFileManagement start {self._path_bat}').startup
        return None




    

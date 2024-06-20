from sys import path
from data import Data
from utils import base_path

class Acess:

    def __init__(self):
        self._name = 'B' # {% builder %}
        self._path = path[0]
        self._path_sign = f'{path[0]}\\sign.txt'
        self._path_settings_strat = f'{path[0]}\\settings.txt'
        self._data_strat = Data.read(self._path_settings_strat)

        adjust_fractal_ticker_off = lambda ticker: ticker.replace('f.sa', '.sa')
        self._ticker = adjust_fractal_ticker_off(self._data_strat[0]) # Train test, results
        
        self._ticker_mt5 = self._data_strat[0].split('.')[0].upper() # Execução

        self._start = self._data_strat[1]
        self._end = self._data_strat[2]
        self._lot = float(self._data_strat[3])

        self._path_settings_control = f'{base_path()}\\Control\\settings.txt'
        self._data_control = Data.read(self._path_settings_control)
        self._update = self._data_control[0]
        self._open = self._data_control[1]
        self._close = self._data_control[2]
        self._after = self._data_control[3]

    








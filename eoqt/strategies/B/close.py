
from acess import Acess
from utils import get_sign
import mt5_operations
import MetaTrader5 as mt5
from log import LogQT

class Close(Acess):

    key = False

    def execution(self):
        match get_sign(self._path_sign):
            case 'buy':
                mt5_operations.order_sell(self._ticker_mt5, self._lot)
            case 'sell':
                mt5_operations.order_buy(self._ticker_mt5, self._lot)
        return True
    
    def loop(self):
        if not(len(mt5.positions_get(symbol=self._ticker_mt5))):
            self.execution()
        return None

if __name__ == '__main__':
    mt5.initialize()
    LogQT('Close start').startup
    Close().loop()
    LogQT('Close end').startup
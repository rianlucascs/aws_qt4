
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
                LogQT('Close Execution (buy)').startup
            case 'sell':
                mt5_operations.order_buy(self._ticker_mt5, self._lot)
                LogQT('Close Execution (sell)').startup
        return True
    
    def loop(self):
        LogQT(f'Close positions_get {len(mt5.positions_get(symbol=self._ticker_mt5))}').startup
        if len(mt5.positions_get(symbol=self._ticker_mt5)) == 1:
            self.execution()
        return None

if __name__ == '__main__':
    mt5.initialize()
    LogQT('Close start').startup
    Close().loop()
    LogQT('Close end').startup

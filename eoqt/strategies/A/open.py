

from acess import Acess
from utils import get_sign, time, timed_out
import mt5_operations
import MetaTrader5 as mt5
from time import sleep
from log import LogQT

class Open(Acess):

    def execution(self):
        match get_sign(self._path_sign):
            case 'buy':
                mt5_operations.order_buy(self._ticker_mt5, self._lot)
                LogQT('Open Execution (buy)').startup
            case 'sell':
                mt5_operations.order_sell(self._ticker_mt5, self._lot)
                LogQT('Open Execution (sell)').startup
        return True

    def loop(self):
        key = False
        to = False
        while True:
            if time() == self._open:
                while True:
                    if not(len(mt5.positions_get(symbol=self._ticker_mt5))):
                        if mt5_operations.barrs(self._ticker_mt5, self._open) == 1:
                            sleep(3.6)
                            key = self.execution()
                            if key:
                                break

                    if timed_out(time()):
                        to = True
                        break
                    
            if key:
                break

            if to:
                LogQT('Open Timed out').startup
                break

if __name__ == '__main__':
    mt5.initialize()
    sleep(5)
    LogQT('Open start').startup
    Open().loop()
    LogQT('Open end').startup

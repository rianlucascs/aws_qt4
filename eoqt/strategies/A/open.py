

from acess import Acess
from utils import get_sign, time, increase
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
        bool_execution = False
        bool_increase_1 = False
        bool_increase_2 = False
        while True:
            sleep(1)
            if time() == self._open:

                print(f'Now = {time()}, Open = {self._open}')

                while True:
                    if not(len(mt5.positions_get(symbol=self._ticker_mt5))):
                        if mt5_operations.barrs(self._ticker_mt5, self._open) == 1:
                            sleep(3.6)
                            bool_execution = self.execution()
                            if bool_execution:
                                break
                    
                    if time() == increase(time(), minutes=10):
                        print('Open bool_increase_1 True')
                        LogQT('Open bool_increase_1 True').startup
                        bool_increase_1 = True

                    if time() == increase(time(), minutes=20):
                        print('Open bool_increase_2 True break')
                        LogQT('Open bool_increase_2 True break 1°').startup
                        bool_increase_2 = True
                        break
                    
                    if bool_increase_1:
                        sleep(10)

            if bool_execution:
                LogQT('Open bool_execution True break').startup
                break

            if bool_increase_2:
                LogQT('Open bool_increase_2 True break 2°').startup
                break

if __name__ == '__main__':
    mt5.initialize()
    LogQT('Open start').startup
    Open().loop()
    LogQT('Open end').startup

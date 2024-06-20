
import MetaTrader5 as mt5 
from datetime import datetime, date, timedelta
from pandas import DataFrame
from os.path import exists
from os import mkdir
from control.utils import writing_file
from sys import path

class TransationLog:
    
    mt5.initialize()

    def __init__(self):
        self.path = f'{path[0]}\\transations\\'

    def date_yesterday(self):
        date_yesterday = datetime.now() - timedelta(days=1)
        date_yesterday = date_yesterday.strftime('%Y-%m-%d').split('-')
        date_yesterday = list(map(int, date_yesterday))
        date_yesterday = datetime(date_yesterday[0], date_yesterday[1], date_yesterday[2], 23, 59, 00)
        return date_yesterday
    
    def date_today(self):
        date_today = list(map(int, datetime.now().strftime('%Y-%m-%d-%H-%M-%S').split('-')))
        date_today = datetime(date_today[0], date_today[1], date_today[2], date_today[3], date_today[4], date_today[5])
        return date_today

    def transation_history(self):
        return mt5.history_deals_get(self.date_yesterday(), self.date_today())
    
    def date_now(self):
        return str(date.today())
    
    def create_directory(self):
        path0 = f'{self.path}\\{date.today().year}' 
        path1 = f'{path0}\\{date.today().month}'
        if not exists(path0):
            mkdir(path0)
            mkdir(path1)
        return path1

    def save(self): 
        filepath = self.create_directory()
        columns = [15, 9, 10, 13, 16]
        data = DataFrame(self.transation_history())[columns].values
        filepath = f'{filepath}\\{self.date_now()}.txt'
        if not exists(filepath):
            for row in range(len(data)):
                info_row = data[row]
                content = f'date={self.date_now()}, ticker={info_row[0]}, lot={info_row[1]}, price={info_row[2]}, result={info_row[3]}, message={info_row[4]}\n'
                writing_file(filepath, content)
        return None
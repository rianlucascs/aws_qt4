
from control.utils import date_today, read_file
from sys import path
from datetime import date
from control.read_transations import ReadTransations

class BuildInfo:

    def __init__(self):
        self._path_transtaion = path[0].replace('\\control', '')+f'\\transations\\{date.today().year}\\{date.today().month}\\{date.today()}.txt'

    @property
    def title_text(self):
        date = date_today().replace('-', '/')
        return f'OVERVIEW SYSTEM STRATEGIES - {date}'
    
    def table_transations(self):
        trf = lambda string: string.split('=')[1]
        file = read_file(self._path_transtaion).split('\n')
        table = [['Ticker', 'Lot', 'Price', 'Result', 'Message']]
        for row in file:
            if row == '':
                break
            row = row.split(', ')
            row = [trf(row[1]), trf(row[2]), trf(row[3]), trf(row[4]), trf(row[5])]
            table.append(row)
        return table
    
    def result_all_strategies(self):
        data = ReadTransations().result('split')
        data = data.reset_index().values
        table = [['Ticker', 'R$']]
        for row in data:
            table.append(row)
        return table

    def risk(self):
        return read_file(f'{path[0]}\\control\\alocation.txt')
        


from sys import path
from os import listdir
from control.utils import read_file
from pandas import DataFrame


class ReadTransations:

    def __init__(self):
        self._path_base = f'{path[0]}\\transations'

    def total_result(self, _path, result=''):
        file = read_file(_path).split('\n')
        sum_result = 0
        list_result = []

        for row in file:
            row = row.split(', ')
            _list = []
            for item in row:
                item = item.split('=')

                match result:
                    case 'sum':
                        if item[0] == 'result':
                            sum_result += float(item[1])

                    case 'split':
                        if item[0] == 'ticker':
                            _list.append(item[1])

                        if item[0] == 'result':
                            _list.append(item[1])
            
            list_result.append(_list)
                
        if result == 'sum':
            return sum_result
        
        elif result == 'split':
            return list_result

    def transform_split_list(self, list_result):
        list_result_ = []
        for list_ in list_result:
            for list__ in list_:
                if not(len(list__)==0):
                    list_result_.append(list__)
        data = DataFrame(list_result_) # Agrupando resultado do francionario com lote cheio 
        data[0] = data[0].apply(lambda ticker: ticker[:-1] if ticker[-1] == 'F' else ticker)
        data[1] = data[1].astype(float)
        data = data.groupby(0).sum()
        return data

    def result(self, result):
        sum_result = 0
        list_result = []
        for year in listdir(self._path_base):
            for month in listdir(f'{self._path_base}\\{year}'):
                for file in listdir(f'{self._path_base}\\{year}\\{month}'):
                    sum_result += self.total_result(f'{self._path_base}\\{year}\\{month}\\{file}', 'sum')
                    list_result.append(self.total_result(f'{self._path_base}\\{year}\\{month}\\{file}', 'split'))
        if result == 'split':
            data = self.transform_split_list(list_result)
            return data
        if result == 'sum':
            return sum_result
                    


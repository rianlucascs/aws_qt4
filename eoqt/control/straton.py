
from os import listdir
from os.path import isdir, join
from sys import path

class StratOn:

    def __init__(self):
        self.strategies_path = join(path[0], 'strategies')

    def names_strategies(self):
        """
        Nomes diretórios arquivos estratégias 
        """
        return [d for d in listdir(self.strategies_path) if isdir(join(self.strategies_path, d))]

    def paths_strategies(self):
        """
        Paths diretórios arquivos estratégias
        """
        return [join(self.strategies_path, d) for d in self.names_strategies()]
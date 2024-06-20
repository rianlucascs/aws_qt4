from model import Model
from utils import writing_file
from acess import Acess
from log import LogQT

class AverageReturn(Acess):

    @staticmethod
    def create():
        LogQT('AverageReturn create').startup
        mean = Model().result_model_after_creation[0]['serie_retorno'].mean()
        writing_file(f'{Acess()._path}\\average_return.txt', mean.__str__(), update=True)


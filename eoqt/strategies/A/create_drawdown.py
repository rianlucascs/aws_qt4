
from model import Model
from utils import writing_file
from acess import Acess
from log import LogQT

class DrawDownMin(Acess):

    @staticmethod
    def create():
        LogQT('DrawDownMin create').startup
        data = Model().result_model_after_creation[0]['serie_retorno']
        drawdawn = data[data < 0].min()
        return writing_file(f'{Acess()._path}\\drawdawn.txt', drawdawn.__str__(), update=True)
        
    
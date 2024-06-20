
from acess import Acess
from model import Model
from utils import writing_file, day_week
from log import LogQT

class CreateSign(Acess):
    
    @property
    def sign(self):
        data = Model().result_model_after_creation[0]
        data = data.iloc[-1]
        
        date =str(data.name)[:10]
        sign = str(data['previsto'])

        if sign == '0' or sign == '0.0':
            return f'{date}, {day_week(date)}, {sign}, sell'
        elif sign == '1' or sign == '1.0':
            return f'{date}, {day_week(date)},{sign}, buy'
        
    def writing_file_sign(self):
        LogQT(f'CreateSign create ({self.sign})').startup
        return writing_file(self._path_sign, self.sign, update=True)
        
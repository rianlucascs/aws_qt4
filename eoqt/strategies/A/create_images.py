from acess import Acess
import matplotlib.pyplot as plt
from utils import date_today
from model import Model
from log import LogQT

class CreateImages(Acess):

    def writing_images_returns_line(self, number_image):
        LogQT(f'CreateImages create {number_image}').startup
        data = Model().result_model_after_creation[0]
        plt.figure(figsize=(6, 5))
        match number_image:
            case 1:
                data['retorno'].cumsum().plot(secondary_y=True, linewidth=0.4, color='black', xlabel='', rot=90, title=f'{date_today()} - {self._ticker.upper()} - {self._name} - {len(data)} days')
                data['retorno_modelo'].plot(xlabel='', rot=90, title=f'{date_today()} - {self._ticker.upper()} - {self._name} - {len(data)} days')
                plt.axvline(x=self._end, linewidth=2, linestyle=':', color='red')
                plt.savefig(f'{self._path}\\image1{self._name}.png')
            case 2:
                data['retorno_modelo'].tail(30).plot(xlabel='', title=f'{date_today()} - {self._ticker.upper()} - {self._name} - 30 days', rot=90)
                plt.savefig(f'{self._path}\\image2{self._name}.png')
        return None
    
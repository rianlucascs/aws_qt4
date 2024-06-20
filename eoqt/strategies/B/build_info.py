

from model import Model
from acess import Acess
from utils import date_today, read_file, day_week
from numpy import where

class BuildInfo(Acess):

    @property
    def title_text(self):
        date = date_today().replace('-', '/')
        return f"REPORT STRATEGY - {self._name} - {date}"

    def settings_table(self):
        content = [
            ['Settings', 'Inputs'],
            ['Ticker', self._ticker],
            ['Start', self._start],
            ['End', self._end],
            ['Lot', self._lot]
        ]
        return content

    def metric_table(self):
        data = Model().model_result_during_creation[1]
        content = [
            ['Metrics', 'Results'],
            ['Train accuracy', f'{data[0]:.2f}'],
            ['Test Accuracy', f'{data[1]:.2f}'],
            ['% Pos.days trian test', f'{data[2]:.3f}'],
            ['% Pos.days test', f'{data[3]:.3f}'],
            ['Aumost of data lost', data[4]],
            ['Number of training signals', f'(Sell {data[5][0]})  (Buy {data[5][1]})'],
            ['Number of test signals', f'(Sell {data[6][0]})  (Buy {data[6][1]})'],
            ['Number of total signals', f'(Sell {data[7][0]})  (Buy {data[7][1]})'],
            ['Overfitting', f'{data[8]:.3f}'],
            ['Average of the series of returns', f'{data[9]:.3f}'],
            ['Standard deviation of returns series', f'{data[10]:.3f}']
        ]
        return content
    
    def result_table(self):
        data = Model().result_model_after_creation[0].reset_index()
        data['Date'] = data['Date'].astype(str)
        data['day_week'] = data['Date'].apply(lambda date: day_week(date))
        data = data[['Date', 'day_week', 'serie_retorno', 'alvo_bin', 'previsto']]
        data['alvo_bin'] = data['alvo_bin'].shift(1).fillna('nan')
        data['alvo_bin'] = data['alvo_bin'].apply(lambda x: int(str(x).replace('.0', '')) if x != 'nan' else 'nan')
        
        data['alvo_bin'] = where(data['alvo_bin'] == 0, 'Sell', 'Buy')
        data['previsto'] = where(data['previsto'] == 0, 'Sell', 'Buy')

        data['R$'] = data['serie_retorno'] * self._lot
        data['R$'] = data['R$'].apply(lambda x: f'{x:.2f}')
        data = data.drop(columns=['serie_retorno']).tail(20).values
        lista = []
        for i, l in enumerate(data):
            if not(i):
                lista.append(['Data', 'Day Week', 'Alvo Bin', 'Previsto', 'R$'])
            else:
                lista.append(list(l))
        return lista

    def last_predict_sign(self):
        return read_file(self._path_sign)

from warnings import filterwarnings
filterwarnings('ignore')

from acess import Acess
from pandas import Timestamp
from datetime import timedelta
from yfinance import download
from datetime import date
from numpy import where
from pandas import DataFrame, concat
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from utils import try_sign
import features as ft

class Model(Acess):

    def inset_features(self, data):
        data["80"] = ft.feature80(data["retorno"])
        data["77"] = ft.feature77(data["retorno"])
        return data
        # {% builder end insert_features %}

    def market_data_train_test(self):
        return download(self._ticker, self._start, self._end, progress=False)[['Adj Close']].rename(columns={'Adj Close': 'adj_close'})

    def market_data(self):
        end = str(Timestamp(str(date.today())) + timedelta(days=20)).split(' ')[0]
        return download(self._ticker, self._start, end, progress=False)[['Adj Close']].rename(columns={'Adj Close': 'adj_close'})

    def _initial_processing(self, data):
        data['retorno'] = data['adj_close'].pct_change(1)
        data['alvo'] = data['retorno'].shift(-1)
        data['centavos'] = data['adj_close'] - data['adj_close'].shift(1)
        data['alvo_bin'] = where(data['alvo'] > 0, 1, 0)
        data = self.inset_features(data)
        return data

    def _split_data(self, data):
        train = data[data.index[0]: data.index[round(data.shape[0] * 0.50)]].dropna()
        test = data[data.index[round(data.shape[0] * 0.50)]: data.index[-1]]
        return [train, test]

    def _create_coef_decision_tree_classifier(self, data_train):
        Tree = DecisionTreeClassifier(criterion='gini', max_depth=3)
        Tree.fit(data_train[data_train.columns[5:].values], data_train.alvo_bin)
        return Tree 

    def _get_coef(self):
        _data = self.market_data_train_test()
        data = self._initial_processing(_data)
        split_data = self._split_data(data)
        coef = self._create_coef_decision_tree_classifier(split_data[0])
        return coef

    def _calculate_returns(self, data):
        data = concat([data[0], data[1]], axis=0) if type(data) == list else data
        data['serie_retorno'] = where(data['previsto'] == 1, data['centavos'], '0')
        data['serie_retorno'] = where(data['previsto'] == 0, -1 * data['centavos'], data['serie_retorno']).astype(float)
        data['retorno_modelo'] = data['serie_retorno'].cumsum() * 100
        return data
    
    def _percentage_positive_days(self, data):
        return (data['serie_retorno'] > 0).value_counts()[True] / len(data)
    
    def _percentage_positive_days_test(self, data):
        return (data[0]['serie_retorno'] > 0).value_counts()[True] / len(data[0])
    
    def _lost_data(self, data, _data):
        return len(data) - len(_data)
    
    def _number_of_signals(self, data, n=0): # n = 0 or 1
        if n != None:
            form = lambda n: list(try_sign(DataFrame(data[n]['previsto']).value_counts()))
            return form(n)
        else:
            form = list(try_sign(DataFrame(data['previsto']).value_counts()))
            return form

    def _overfitting(self, x, y):
        return abs(x - y)
    
    def _mean_serie_retorno(self, data):
        return data['serie_retorno'].mean()
    
    def _std_serie_retorno(self, data):
        return data['serie_retorno'].std()

    def _metric_result_during_creation(self, data, _data):
        __data = self._split_data(data)
        return [
            x:= accuracy_score(__data[0]['alvo_bin'], __data[0]['previsto']) * 100,
            y:= accuracy_score(__data[1]['alvo_bin'], __data[1]['previsto']) * 100,
            self._percentage_positive_days(data),
            self._percentage_positive_days_test(__data),
            self._lost_data(data, _data),
            self._number_of_signals(__data, 0), 
            self._number_of_signals(__data, 1),
            self._number_of_signals(data, None),
            self._overfitting(x, y),
            self._mean_serie_retorno(data),
            self._std_serie_retorno(data)
        ]

    @property
    def model_result_during_creation(self):
        _data = self.market_data_train_test()
        data = self._initial_processing(_data)
        split_data = self._split_data(data)
        coef = self._create_coef_decision_tree_classifier(split_data[0])
        predict_train = coef.predict(split_data[0][split_data[0].columns[5:]])
        predict_test = coef.predict(split_data[1][split_data[1].columns[5:]])
        split_data[0]['previsto'] = predict_train
        split_data[1]['previsto'] = predict_test
        data = self._calculate_returns(split_data)
        metric = self._metric_result_during_creation(data, _data)
        return [data, metric]

    def metric_result_model_after_creation(self, data):
        """Metricas referentes aos resultados pós treino"""
        return [
            self._number_of_signals(data, None),
            self._mean_serie_retorno(data),
            self._std_serie_retorno(data)
        ]

    @property
    def result_model_after_creation(self):
        data = self.market_data()
        data = self._initial_processing(data)
        coef = self._get_coef()
        data['previsto'] = coef.predict(data[data.columns[5:]])
        data = self._calculate_returns(data)
        _data = data[len(self.market_data_train_test()):]
        metric = self.metric_result_model_after_creation(_data)
        return [data, metric]
    
# print(Model().writing_images(3))


""""
>>> Ajustar o tamnho do lot por capital alocado
"""

import MetaTrader5 as mt5 
from yfinance import download
from control.straton import StratOn
from control.utils import read_file, writing_file
from sys import path
from control.log import LogQt

class Risk:
    
    def __init__(self):
        mt5.initialize()
        self.adjust_fractal_ticker_off = lambda ticker: ticker.replace('f.sa', '.sa')
        self.adjust_fractal_ticker_on =  lambda ticker: ticker.replace('.sa', 'f.sa')

    def account_info(self):
        return mt5.account_info()

    def capital_available_for_allocation(self):
        return self.account_info().balance / 2
    
    def capital_allocated_to_each_strategy(self):
        return self.capital_available_for_allocation() / len(StratOn().names_strategies())

    def last_price(self, ticker):
        return download(ticker, period='1y', progress=False)[['Adj Close']].values[0][0]
    
    def quantity_of_active_strategies(self):
        return len(StratOn().names_strategies())

    def info_strats(self):
        info = []
        for _path in StratOn().paths_strategies():
            ticker = read_file(f'{_path}\\settings.txt').split(', ')[0]
            ticker = self.adjust_fractal_ticker_off(ticker)
            drawdrawns = read_file(f'{_path}\\drawdawn.txt')
            average_return = read_file(f'{_path}\\average_return.txt')
            info.append([_path[-1], ticker, float(drawdrawns), float(average_return), _path])
        return info
    
    def options_risk(self, ticker, Projected_Risk, max_loss):
        """
        >>> Pondera o prejuizo maximo 'toleravel' definido manualmente 'max_loss'
        >>> E a quantidade de capital 'capital_allocated_to_each_strategy' disponível para cada estratégia
        """
        list_lot = range(1, 10000)
        list_result = []
        for n in list_lot:
            if n <= 100 or str(n).endswith('00') or str(n).endswith('000'):
                calc = n*self.last_price(ticker) * (Projected_Risk / 100)
                if abs(calc) <= max_loss:
                    cost = self.last_price(ticker) * n
                    if cost <= self.capital_allocated_to_each_strategy():
                        list_result.append([n, calc, cost])
        return list_result

    def average_return_based_on_risk(self, lot, average_return):
        return lot * average_return

    def risk_adjustment(self, lot, _path):
        _path = f'{_path}\\settings.txt'
        file = read_file(_path).split(', ')
        file[3] = lot
        if lot < 100: 
            if not 'f.sa' in file[0]:
                file[0] = self.adjust_fractal_ticker_on(file[0])
        else:
            if 'f.sa' in file[0]:
                file[0] = self.adjust_fractal_ticker_off(file[0])
        file = [str(item) for item in file]
        file = ', '.join(file)
        writing_file(_path, file, update=True)


    def protocol1(self):
        LogQt('Risk create').startup
        projected = 4 # Multiplicador do maior prejuizo
        max_loss = 100 # Limite financeiro
        
        content = f'projected: {projected}x<br />max_loss: R$ {max_loss}'
        for name, ticker, drawdrawn, average_return, _path in self.info_strats():
            Projected_Risk = drawdrawn * projected
            options_risk = self.options_risk(ticker, Projected_Risk, max_loss)[-1]
            lot = options_risk[0]
            calc = options_risk[1]
            cost = options_risk[2]
            average_return_based_on_risk = self.average_return_based_on_risk(lot, average_return)
            self.risk_adjustment(lot, _path)
            content += f'<br /><br />Ticker: {ticker}<br />Lot: {lot}<br />Calc: {calc:.2f}<br />Cost: R$ {cost:.2f}<br />Limit cost: R$ {self.capital_allocated_to_each_strategy()}<br />Average return based on risk: {average_return_based_on_risk:.2f}'
        
        writing_file(f'{path[0]}\\control\\alocation.txt', content, update=True)

# Risk().protocol1()
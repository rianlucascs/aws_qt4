import MetaTrader5 as mt5 
from datetime import datetime
from pandas import Timestamp, DataFrame, to_datetime

def order_buy(ticker, lot):
    mt5.initialize()
    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': ticker,
        'volume': float(lot),
        'type': mt5.ORDER_TYPE_BUY,
        'price': mt5.symbol_info_tick(ticker).last,
        'deviation': 0,
        'magic': 234000,
        'comment': 'Buy',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN}
    resultado = mt5.order_send(request)
    return resultado

def order_sell(ticker, lot):
    mt5.initialize()
    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': ticker,
        'volume': float(lot),
        'type': mt5.ORDER_TYPE_SELL,
        'price': mt5.symbol_info_tick(ticker).last,
        'deviation': 0,
        'magic': 234000,
        'comment': 'Sell',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_RETURN}
    resultado = mt5.order_send(request)
    return resultado

def barrs(ativo, _open):
    mt5.initialize()
    data_hoje_pregao = datetime.today().strftime('%Y-%m-%d') + f'-{_open}' # <--!!! # -10:00:00
    diff_inicio_pregao = datetime.today() - Timestamp(data_hoje_pregao)
    quantidade_barras = int(diff_inicio_pregao.total_seconds() / (1 * 60))
    barras_frame = DataFrame(mt5.copy_rates_from(ativo, mt5.TIMEFRAME_M1, datetime.today(), quantidade_barras))
    barras_frame['time'] = to_datetime(barras_frame['time'], unit='s')
    barras_hoje = barras_frame[barras_frame['time'] >= data_hoje_pregao].reset_index(drop=True)
    return len(barras_hoje)

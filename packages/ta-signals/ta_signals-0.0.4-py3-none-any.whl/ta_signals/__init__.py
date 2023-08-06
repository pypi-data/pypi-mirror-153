from .main import TaSignals

def go(ohlc, key, window=2, front_run=.05):
    t = TaSignals()

    ma_data, ohlc = t.ma(ohlc, key, window, front_run)
    ema_data, ohlc = t.ema(ohlc, key, window, front_run)
    bollinger_data, ohlc = t.bollinger(ohlc, key, window, front_run)
    rsi_data, ohlc = t.rsi(ohlc, key, window, front_run)
    macd_data, ohlc = t.macd_slope(ohlc, key, window, front_run)
    div_data, ohlc = t.divergence(ohlc, key, window, front_run)
    #obv_data, ohlc = t.on_balance_volume(ohlc, 5, key, window, front_run)

    data = div_data + bollinger_data + macd_data + ma_data + ema_data + rsi_data

    return data, ohlc


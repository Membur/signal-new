import os
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from indicator_functions import calculate_rsi, calculate_macd, calculate_stochastic, calculate_cci, calculate_mfi
from constants import (
    rsi_oversold,
    rsi_overbought,
    macd_threshold,
    stoch_oversold,
    stoch_overbought,
    cci_oversold,
    cci_overbought,
    mfi_oversold,
    mfi_overbought,
)

def get_most_recent_signals(data):
    signals = []
    calculate_rsi(data)
    calculate_macd(data)
    calculate_stochastic(data)
    calculate_cci(data)
    calculate_mfi(data)

    # Calculate RSI signals
    rsi_buy_signal = (data['RSI'].iloc[-1] < rsi_oversold)
    rsi_sell_signal = (data['RSI'].iloc[-1] > rsi_overbought)
    signals.append(('RSI Buy', rsi_buy_signal))
    signals.append(('RSI Sell', rsi_sell_signal))

    # Calculate MACD signals
    macd_buy_signal = (data['MACD'].iloc[-1] > macd_threshold)
    macd_sell_signal = (data['MACD'].iloc[-1] < macd_threshold)
    signals.append(('MACD Buy', macd_buy_signal))
    signals.append(('MACD Sell', macd_sell_signal))

    # Calculate Stochastic signals
    stoch_buy_signal = (data['Stochastic_K'].iloc[-1] < stoch_oversold)
    stoch_sell_signal = (data['Stochastic_K'].iloc[-1] > stoch_overbought)
    signals.append(('Stochastic Buy', stoch_buy_signal))
    signals.append(('Stochastic Sell', stoch_sell_signal))

    # Calculate CCI signals
    cci_buy_signal = (data['CCI'].iloc[-1] < cci_oversold)
    cci_sell_signal = (data['CCI'].iloc[-1] > cci_overbought)
    signals.append(('CCI Buy', cci_buy_signal))
    signals.append(('CCI Sell', cci_sell_signal))

    # Calculate MFI signals
    mfi_buy_signal = (data['MFI'].iloc[-1] < mfi_oversold)
    mfi_sell_signal = (data['MFI'].iloc[-1] > mfi_overbought)
    signals.append(('MFI Buy', mfi_buy_signal))
    signals.append(('MFI Sell', mfi_sell_signal))

    return signals
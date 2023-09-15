import talib

def calculate_rsi(data):
    data['RSI'] = talib.RSI(data['Close'])
    return data  # Return the modified DataFrame

def calculate_macd(data):
    data['MACD'], _, _ = talib.MACD(data['Close'])
    return data  # Return the modified DataFrame

def calculate_stochastic(data):
    data['Stochastic_K'], data['Stochastic_D'] = talib.STOCH(data['High'], data['Low'], data['Close'])
    return data  # Return the modified DataFrame

def calculate_cci(data):
    data['CCI'] = talib.CCI(data['High'], data['Low'], data['Close'])
    return data  # Return the modified DataFrame

def calculate_mfi(data):
    data['MFI'] = talib.MFI(data['High'], data['Low'], data['Close'], data['Volume'])
    return data  # Return the modified DataFrame

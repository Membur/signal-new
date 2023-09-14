import os
import yfinance as yf
import pandas as pd
from candlestick_detection import detect_candlestick_pattern
from indicator_functions import calculate_rsi, calculate_macd, calculate_stochastic, calculate_cci, calculate_mfi
from signal_functions import get_most_recent_signals
from chart_functions import generate_chart
from constants import (
    rsi_oversold, rsi_overbought, macd_threshold, stoch_oversold, stoch_overbought,
    cci_oversold, cci_overbought, mfi_oversold, mfi_overbought, min_volume
)

# Define a main function
def main():
    data_dir = 'C:/Users/Sean/Documents/Python Scripts/pinter-new-try/charts'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, '1wk-charts'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, '1wk-data'), exist_ok=True)

    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]

            try:
                data = yf.download(symbol, start="2022-10-01", end="2023-08-09", interval="1wk")

                # Define detected_patterns here
                open_prices = data['Open']
                high_prices = data['High']
                low_prices = data['Low']
                close_prices = data['Close']
                detected_patterns = detect_candlestick_pattern(open_prices, high_prices, low_prices, close_prices)

                # Print detected patterns
                if detected_patterns:
                    print(f"Detected Candlestick Patterns for {symbol}:")
                    for pattern in detected_patterns:
                        print(pattern)
                else:
                    print(f"No patterns detected for {symbol}.")

                generate_chart(
                    symbol,
                    data,
                    data_dir=data_dir,
                    min_indicators=1,
                    min_volume=min_volume,  # Pass the minimum volume threshold
                )
            except Exception as e:
                print(f"Failed to generate chart for symbol {symbol}: {e}")

if __name__ == "__main__":
    main()
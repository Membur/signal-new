import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Define the SYMBOLS, START_DATE, and END_DATE directly in this script
SYMBOLS = ['AMD']
START_DATE = "2022-09-19"
END_DATE = "2022-11-15"

# Define the directory where you want to save the CSV files
SAVE_DIRECTORY = r'C:\Users\Sean\Documents\Python Scripts\Sean-Screener\charts\fetched-data'

def fetch_data(symbol, start_date, end_date):
    try:
        # Download data using yfinance
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        # Calculate buy and sell volumes
        data['Buy Volume'] = data['Volume'] * (data['Close'] >= data['Open'])
        data['Sell Volume'] = data['Volume'] * (data['Close'] < data['Open'])
        
        # Add candlestick data
        data['Open'] = data['Open']
        data['Close'] = data['Close']
        
        # Apply technical analysis indicators
        data.ta.macd(append=True, fast=12, slow=26, signal=9)
        data.ta.rsi(append=True)
        
        # Add more indicators as needed
        
        return data

    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")
        return None

# Define a function to save data to CSV
def save_data_to_csv(data, filename):
    try:
        # Ensure that the directory exists, create it if not
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)
        # Create the full path to the CSV file
        full_path = os.path.join(SAVE_DIRECTORY, filename)
        data.to_csv(full_path)
        print(f"Data saved to {full_path}")

    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

if __name__ == "__main__":
    for symbol in SYMBOLS:
        # Fetch data
        data = fetch_data(symbol, START_DATE, END_DATE)

        if data is not None:
            # Save the data to a CSV file in the specified directory
            save_data_to_csv(data, f"{symbol}_data.csv")

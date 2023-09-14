import talib
import pandas as pd

# Import the candlestick patterns dictionary from patterns.py (assuming it's in the same directory)
from patterns import candlestick_patterns

def detect_candlestick_pattern(open_prices, high_prices, low_prices, close_prices):
    try:
        # Initialize a list to store detected patterns
        detected_patterns = []

        # Iterate through the candlestick patterns dictionary
        for pattern_name, pattern_description in candlestick_patterns.items():
            pattern_function = getattr(talib, pattern_name)

            # Calculate the candlestick pattern using talib
            candlestick_results = pattern_function(open_prices, high_prices, low_prices, close_prices)

            # Check if the last result is greater than 0 (bullish pattern)
            if candlestick_results.iloc[-1] > 0:
                detected_patterns.append(f"Bullish {pattern_description}")
            
            # Check if the last result is less than 0 (bearish pattern)
            elif candlestick_results.iloc[-1] < 0:
                detected_patterns.append(f"Bearish {pattern_description}")

        return detected_patterns

    except Exception as e:
        print('Failed with error:', e)
        return None

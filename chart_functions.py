import os
import plotly.graph_objs as go
import os
import yfinance as yf
import pandas as pd
from indicator_functions import calculate_rsi, calculate_macd, calculate_stochastic, calculate_cci, calculate_mfi
from signal_functions import get_most_recent_signals
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


def generate_chart(symbol, data, data_dir, min_indicators=1, min_volume=None):
    
    # Assuming you have OHLC data loaded in variables open_prices, high_prices, low_prices, and close_prices
    detected_patterns = detect_candlestick_pattern(open_prices, high_prices, low_prices, close_prices)

    # Check the minimum volume threshold
    if min_volume is not None and data['Volume'].iloc[-1] < min_volume:
        print(f"Volume for {symbol} is below the minimum threshold. Skipping...")
        return

    signals = get_most_recent_signals(data)

    # Check if at least min_indicators indicators generated signals
    active_signals = [indicator for indicator, signal in signals if signal]
    if len(active_signals) < min_indicators:
        print(f"Not enough active signals ({len(active_signals)}) for {symbol}. Skipping...")
        return

    data.to_csv(os.path.join(data_dir, '1wk-data', f'{symbol}_data.csv'))

    fig = go.Figure()

    candlestick = go.Candlestick(
        x=data.index.astype(str),
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red'
    )

    fig.add_trace(candlestick)

    vertical_offset = 0  # Initialize vertical offset

    for indicator, signal in signals:
        if 'Buy' in indicator and signal:
            signal_arrow = go.Scatter(
                x=[data.index[-1]],
                y=[data['Low'].iloc[-1] + vertical_offset],  # Apply vertical offset
                mode='markers+text',
                marker=dict(symbol='triangle-up', size=12, color='green'),
                text=['BUY'],
                textposition="bottom center",
                name=f'{indicator} Signal'
            )

            fig.add_trace(signal_arrow)

            vertical_offset += 0.5  # Adjust the vertical offset for the next indicator

        if 'Sell' in indicator and signal:
            signal_arrow = go.Scatter(
                x=[data.index[-1]],
                y=[data['Low'].iloc[-1] - vertical_offset],  # Apply vertical offset
                mode='markers+text',
                marker=dict(symbol='triangle-down', size=12, color='red'),
                text=['SELL'],
                textposition="bottom center",
                name=f'{indicator} Signal'
            )

            fig.add_trace(signal_arrow)

            vertical_offset += 0.5  # Adjust the vertical offset for the next indicator

    title_text = f'<a href="https://www.tradingview.com/symbols/{symbol}/" target="_blank">{symbol}</a> 1 Week Signals'

    fig.update_layout(
        title=title_text,
        xaxis_title="Date",
        yaxis_title="Price",
        showlegend=True,
        template='plotly_dark'
    )

    chart_file = os.path.join(data_dir, '1wk-charts', f'{symbol}_signals_1wk.html')
    fig.write_html(chart_file)
    print(f"Chart saved as {chart_file}")

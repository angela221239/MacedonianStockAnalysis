import pandas as pd
import numpy as np


def calculate_sma(data, window=14):
    """Calculates the Simple Moving Average (SMA)."""
    return data['Close'].rolling(window=window, min_periods=1).mean()


def calculate_rsi(data, window=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=window, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=window, min_periods=1).mean()

    rs = avg_gain / (avg_loss + 1e-10)  # Avoid division by zero
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """Calculates the MACD (Moving Average Convergence Divergence) indicator."""
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()

    return macd, signal


def perform_technical_analysis(data):
    """
    Performs technical analysis by calculating SMA, RSI, and MACD.

    Parameters:
    - data (DataFrame): Stock price data.

    Returns:
    - DataFrame with additional columns for SMA, RSI, MACD, and Signal Line.
    """
    if len(data) < 5:
        raise ValueError("Not enough data for technical analysis. At least 5 rows required.")

    data = data.copy()

    #  Convert Date column to datetime (Fixes issue with sorting & calculations)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)

    #  Ensure "Close" column exists (Fix for "price" JSON format)
    if 'price' in data.columns:
        data.rename(columns={'price': 'Close'}, inplace=True)

    #  Ensure Close prices are float values
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

    #  Calculate SMA
    data['SMA_14'] = calculate_sma(data, window=14)

    #  Calculate RSI
    data['RSI_14'] = calculate_rsi(data, window=14)

    #  Calculate MACD
    data['MACD'], data['MACD_Signal'] = calculate_macd(data)

    #  Drop NaN rows after calculations
    return data[['Date', 'Close', 'SMA_14', 'RSI_14', 'MACD', 'MACD_Signal']].dropna()

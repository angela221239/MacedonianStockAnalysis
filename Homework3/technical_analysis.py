from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator


def calculate_sma(data, window):
    """Calculate Simple Moving Average (SMA)."""
    sma = SMAIndicator(data['Close'], window=window)
    return sma.sma_indicator()


def calculate_ema(data, window):
    """Calculate Exponential Moving Average (EMA)."""
    ema = EMAIndicator(data['Close'], window=window)
    return ema.ema_indicator()


def calculate_rsi(data, window):
    """Calculate Relative Strength Index (RSI)."""
    rsi = RSIIndicator(data['Close'], window=window)
    return rsi.rsi()


def perform_technical_analysis(data):
    """
    Perform technical analysis on the given stock data.
    Adds SMA, EMA, and RSI columns and generates buy/sell signals.

    Parameters:
    - data: DataFrame containing stock data with a 'Close' column.

    Returns:
    - DataFrame with added indicators and signals.
    """
    # Validate input data
    if 'Close' not in data.columns:
        raise ValueError("Input data must contain a 'Close' column.")

    # Calculate indicators
    data['SMA_20'] = calculate_sma(data, 20)
    data['EMA_20'] = calculate_ema(data, 20)
    data['RSI_14'] = calculate_rsi(data, 14)

    # Generate buy/sell signals
    data['Buy Signal'] = (data['RSI_14'] < 30) & (data['Close'] > data['SMA_20'])
    data['Sell Signal'] = (data['RSI_14'] > 70) & (data['Close'] < data['SMA_20'])

    return data

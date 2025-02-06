import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split


def load_stock_data(issuer_code):
    """
    Loads stock price data from JSON files in Homework3popravka/src/data/.

    Parameters:
    - issuer_code: The stock issuer code (used to find the correct JSON file).

    Returns:
    - DataFrame containing stock prices.
    """
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_folder, f"{issuer_code}.json")

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No data found for issuer: {issuer_code}. Expected file: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            stock_data = json.load(f)

        # Ensure JSON file is a list of dictionaries
        if not isinstance(stock_data, list):
            raise ValueError(f"Invalid JSON format in {file_path}. Expected a list, got {type(stock_data)}")

        # Convert JSON into a DataFrame
        all_data = []
        for entry in stock_data:
            if isinstance(entry, dict) and 'date' in entry:
                # Use 'price' if 'close' is missing
                price = entry.get('close', entry.get('price'))  # Check both keys
                if price is not None:
                    all_data.append({'Date': entry['date'], 'Close': price})

        # Raise error if no valid stock data
        if not all_data:
            raise ValueError(f"No valid stock data found in {file_path}. Ensure 'date' and 'price' exist.")

        df = pd.DataFrame(all_data)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        return df

    except json.JSONDecodeError:
        raise ValueError(f"Error reading JSON file: {file_path}. Invalid JSON format.")


def preprocess_data(data, look_back=30):
    """
    Prepares the stock data for training and prediction.

    Parameters:
    - data: DataFrame containing stock prices with a 'Close' column.
    - look_back: Number of previous time steps to use for prediction.

    Returns:
    - X_train, X_test, y_train, y_test: Training and testing sets.
    - scaler: The fitted MinMaxScaler object.
    """
    if 'Close' not in data.columns:
        raise ValueError("Data must contain a 'Close' column.")

    # Adjust look_back dynamically to fit available data
    look_back = min(look_back, len(data))

    if len(data) < 2:
        raise ValueError(f"Not enough data. At least 2 rows required, but got {len(data)}.")

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['Close']])

    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i - look_back:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)

    # Ensure correct shape even with small datasets
    if len(X) == 0:
        X = np.zeros((1, look_back))  # Create a dummy input if no valid data exists
        y = np.zeros(1)

    # Avoid errors with very small datasets
    if len(X) < 2:
        return X, X, y, y, scaler  # Return all data for training

    # Dynamically adjust test size for small datasets
    test_size = min(0.2, len(X) - 1) if len(X) > 5 else 1

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    return X_train, X_test, y_train, y_test, scaler


def train_xgb_model(X_train, y_train):
    model = XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train, y_train)
    return model


def predict_future_prices(model, recent_data, scaler, steps=10):
    predictions = []
    input_data = recent_data[-30:].reshape(1, -1)

    for _ in range(steps):
        predicted_price = float(model.predict(input_data)[0])
        predictions.append(predicted_price)
        input_data = np.append(input_data[:, 1:], predicted_price).reshape(1, -1)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions

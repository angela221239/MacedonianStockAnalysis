import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def preprocess_data(data, look_back=30):
    """
    Preprocess the stock data for LSTM input.

    Parameters:
    - data: DataFrame containing stock prices with a 'Close' column.
    - look_back: Number of previous time steps to use for prediction.

    Returns:
    - X, y: Features and labels for training/testing.
    - scaler: Fitted MinMaxScaler object.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i - look_back:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)

    # Reshape X to be [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler


def build_lstm_model(input_shape):
    """
    Build an LSTM model.

    Parameters:
    - input_shape: Shape of the input data (look_back, 1).

    Returns:
    - model: Compiled LSTM model.
    """
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def train_lstm_model(X_train, y_train, input_shape, epochs=10, batch_size=32):
    """
    Train the LSTM model.

    Parameters:
    - X_train: Training features.
    - y_train: Training labels.
    - input_shape: Shape of the input data.
    - epochs: Number of training epochs.
    - batch_size: Size of training batches.

    Returns:
    - model: Trained LSTM model.
    """
    model = build_lstm_model(input_shape)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model


def predict_future_prices(model, recent_data, scaler, steps=30):
    """
    Predict future stock prices.

    Parameters:
    - model: Trained LSTM model.
    - recent_data: Recent data (scaled) to base predictions on.
    - scaler: Fitted MinMaxScaler object.
    - steps: Number of future steps to predict.

    Returns:
    - predictions: Predicted stock prices (scaled back to original values).
    """
    predictions = []
    input_data = recent_data[-30:].reshape(1, 30, 1)

    for _ in range(steps):
        # Predict the next price
        predicted_price = model.predict(input_data, verbose=0)[0, 0]
        predictions.append(predicted_price)

        # Prepare input for the next prediction
        input_data = np.append(input_data[:, 1:, :], [[[predicted_price]]], axis=1)

    # Scale predictions back to original values
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions

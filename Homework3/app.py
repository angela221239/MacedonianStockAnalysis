from flask import Flask, jsonify, request
from technical_analysis import perform_technical_analysis
from fundamental_analysis import analyze_sentiment
from lstm_prediction import build_lstm_model
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return """
    <h1>Macedonian Stock Analysis</h1>
    <p>Endpoints:</p>
    <ul>
        <li><b>GET /technical_analysis</b>: Perform technical analysis on stock data.</li>
        <li><b>POST /fundamental_analysis</b>: Perform fundamental analysis on input text.</li>
        <li><b>GET /lstm_prediction</b>: Predict stock prices using an LSTM model.</li>
    </ul>
    """


# Technical Analysis endpoint
@app.route('/technical_analysis', methods=['GET'])
def technical_analysis():
    try:
        # Example stock data (replace with actual data from a CSV or API)
        data = pd.DataFrame({
            'Date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05'],
            'Close': [100, 102, 104, 103, 105]
        })

        # Perform technical analysis
        analyzed_data = perform_technical_analysis(data)

        # Convert results to JSON and return
        result = analyzed_data.to_dict(orient='records')
        return jsonify({'status': 'success', 'data': result})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# Fundamental Analysis endpoint
@app.route('/fundamental_analysis', methods=['POST'])
def fundamental_analysis():
    try:
        # Get text input from the request
        input_data = request.json
        text = input_data.get('text', '')

        if not text:
            return jsonify({'status': 'error', 'message': 'No text provided'}), 400

        # Perform sentiment analysis
        sentiment = analyze_sentiment(text)
        return jsonify({'status': 'success', 'sentiment': sentiment})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# LSTM Prediction endpoint
@app.route('/lstm_prediction', methods=['GET'])
def lstm_prediction():
    try:
        # Example input shape for LSTM (replace with actual data)
        input_shape = (30, 1)

        # Build LSTM model
        model = build_lstm_model(input_shape)

        # Return a success message (replace with actual predictions later)
        return jsonify({'status': 'success', 'message': 'LSTM model built successfully'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

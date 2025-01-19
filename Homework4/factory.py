# factory.py
from technical_analysis import perform_technical_analysis
from fundamental_analysis import analyze_sentiment
from lstm_prediction import build_lstm_model


class AnalysisFactory:
    @staticmethod
    def get_technical_analysis(data):
        """
        Create a technical analysis object with the given data.
        """
        return perform_technical_analysis(data)

    @staticmethod
    def get_sentiment_analysis(text):
        """
        Perform sentiment analysis on the given text.
        """
        return analyze_sentiment(text)

    @staticmethod
    def get_lstm_model(input_shape):
        """
        Create an LSTM model with the specified input shape.
        """
        return build_lstm_model(input_shape)

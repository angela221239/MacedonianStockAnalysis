import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Download required NLTK data (only needed once)
nltk.download('vader_lexicon')


def clean_text(text):
    """
    Cleans input text by removing special characters, extra spaces, and converting to lowercase.

    Parameters:
    - text (str): The raw input text.

    Returns:
    - str: Cleaned text.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text related to stock market fundamentals.

    Parameters:
    - text (str): The input text for sentiment analysis.

    Returns:
    - dict: Contains sentiment score and classification (positive, neutral, or negative).
    """
    if not text or not isinstance(text, str):
        return {"error": "Invalid text input. Please provide a valid string."}

    # ✅ Clean the input text
    cleaned_text = clean_text(text)

    # ✅ Initialize Sentiment Intensity Analyzer (VADER)
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(cleaned_text)

    # ✅ Classify sentiment based on compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = "positive"
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "text": text,
        "cleaned_text": cleaned_text,
        "sentiment": sentiment,
        "scores": sentiment_scores  # Includes compound, pos, neu, neg
    }

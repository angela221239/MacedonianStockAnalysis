from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text.

    Parameters:
    - text (str): The text to analyze.

    Returns:
    - str: The sentiment of the text ('positive', 'negative', or 'neutral').
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'
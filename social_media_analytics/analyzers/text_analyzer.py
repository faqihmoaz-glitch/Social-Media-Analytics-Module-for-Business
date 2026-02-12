"""
Text Sentiment Analysis Module
- Uses VADER for social media text
- Uses TextBlob for general text
- Supports multiple languages
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import pandas as pd

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)


class TextAnalyzer:
    """
    Comprehensive text analysis for social media posts.
    
    Features:
        - Sentiment Analysis (VADER + TextBlob)
        - Keyword Extraction
        - Hashtag Analysis
        - Mention Analysis
        - Text Cleaning & Preprocessing
    """

    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

    # ──────────────────────────────────────────
    # Text Preprocessing
    # ──────────────────────────────────────────
    def clean_text(self, text):
        """Remove URLs, mentions, special characters from text."""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtag symbol (keep the word)
        text = re.sub(r'#', '', text)
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()

    def extract_hashtags(self, text):
        """Extract all hashtags from text."""
        return re.findall(r'#(\w+)', text)

    def extract_mentions(self, text):
        """Extract all @mentions from text."""
        return re.findall(r'@(\w+)', text)

    def extract_urls(self, text):
        """Extract all URLs from text."""
        return re.findall(r'http[s]?://\S+', text)

    # ──────────────────────────────────────────
    # Sentiment Analysis
    # ──────────────────────────────────────────
    def analyze_sentiment_vader(self, text):
        """
        Analyze sentiment using VADER (optimized for social media).
        
        Returns:
            dict: Sentiment scores (positive, negative, neutral, compound)
        """
        scores = self.vader_analyzer.polarity_scores(text)

        # Classify based on compound score
        if scores['compound'] >= 0.05:
            sentiment_label = 'Positive'
        elif scores['compound'] <= -0.05:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'

        return {
            'text': text,
            'scores': scores,
            'label': sentiment_label,
            'compound': scores['compound'],
            'confidence': abs(scores['compound'])
        }

    def analyze_sentiment_textblob(self, text):
        """
        Analyze sentiment using TextBlob.
        
        Returns:
            dict: Polarity (-1 to 1) and Subjectivity (0 to 1)
        """
        blob = TextBlob(text)

        if blob.sentiment.polarity > 0.05:
            label = 'Positive'
        elif blob.sentiment.polarity < -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'

        return {
            'text': text,
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'label': label
        }

    def combined_sentiment(self, text):
        """
        Combine VADER and TextBlob for more accurate sentiment analysis.
        """
        vader_result = self.analyze_sentiment_vader(text)
        textblob_result = self.analyze_sentiment_textblob(text)

        # Weighted average (VADER weighted more for social media)
        combined_score = (
            vader_result['compound'] * 0.6 +
            textblob_result['polarity'] * 0.4
        )

        if combined_score >= 0.05:
            label = 'Positive'
        elif combined_score <= -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'

        return {
            'text': text,
            'vader_score': vader_result['compound'],
            'textblob_polarity': textblob_result['polarity'],
            'textblob_subjectivity': textblob_result['subjectivity'],
            'combined_score': combined_score,
            'label': label,
            'confidence': abs(combined_score)
        }

    # ──────────────────────────────────────────
    # Keyword Extraction
    # ──────────────────────────────────────────
    def extract_keywords(self, text, top_n=20):
        """Extract most frequent meaningful keywords."""
        cleaned = self.clean_text(text)
        tokens = word_tokenize(cleaned)

        # Remove stopwords and short words
        keywords = [
            word for word in tokens
            if word not in self.stop_words and len(word) > 2
        ]

        return Counter(keywords).most_common(top_n)

    # ──────────────────────────────────────────
    # Batch Analysis
    # ──────────────────────────────────────────
    def analyze_batch(self, texts):
        """
        Analyze multiple texts and return a DataFrame with results.
        """
        results = []
        for text in texts:
            result = self.combined_sentiment(text)
            result['hashtags'] = self.extract_hashtags(text)
            result['mentions'] = self.extract_mentions(text)
            results.append(result)

        df = pd.DataFrame(results)
        return df

    def get_sentiment_summary(self, df):
        """Generate summary statistics from batch analysis."""
        summary = {
            'total_posts': len(df),
            'positive_count': len(df[df['label'] == 'Positive']),
            'negative_count': len(df[df['label'] == 'Negative']),
            'neutral_count': len(df[df['label'] == 'Neutral']),
            'avg_sentiment': df['combined_score'].mean(),
            'sentiment_std': df['combined_score'].std(),
            'most_positive': df.loc[df['combined_score'].idxmax(), 'text'] if len(df) > 0 else None,
            'most_negative': df.loc[df['combined_score'].idxmin(), 'text'] if len(df) > 0 else None,
            'positive_percentage': (len(df[df['label'] == 'Positive']) / len(df) * 100) if len(df) > 0 else 0,
            'negative_percentage': (len(df[df['label'] == 'Negative']) / len(df) * 100) if len(df) > 0 else 0,
            'neutral_percentage': (len(df[df['label'] == 'Neutral']) / len(df) * 100) if len(df) > 0 else 0,
        }
        return summary
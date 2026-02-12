"""
Configuration file for Social Media Analytics Module
"""

import os

# ──────────────────────────────────────────────
# Directory Configuration
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
WORDCLOUD_DIR = os.path.join(OUTPUT_DIR, "wordclouds")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, CHARTS_DIR, WORDCLOUD_DIR, REPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ──────────────────────────────────────────────
# Sentiment Analysis Configuration
# ──────────────────────────────────────────────
SENTIMENT_THRESHOLDS = {
    "positive": 0.05,
    "negative": -0.05
}

# ──────────────────────────────────────────────
# Social Media API Keys (Replace with actual keys)
# ──────────────────────────────────────────────
API_KEYS = {
    "twitter": {
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET",
        "access_token": "YOUR_ACCESS_TOKEN",
        "access_secret": "YOUR_ACCESS_SECRET"
    },
    "facebook": {
        "app_id": "YOUR_APP_ID",
        "app_secret": "YOUR_APP_SECRET"
    }
}

# ──────────────────────────────────────────────
# Word Cloud Configuration
# ──────────────────────────────────────────────
WORDCLOUD_CONFIG = {
    "width": 800,
    "height": 400,
    "max_words": 200,
    "background_color": "white",
    "colormap": "viridis"
}
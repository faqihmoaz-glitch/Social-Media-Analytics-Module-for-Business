"""
Word Cloud Generation Module
- Standard word clouds
- Sentiment-colored word clouds
- Shaped word clouds
- Hashtag clouds
"""

import os
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from config import WORDCLOUD_DIR, WORDCLOUD_CONFIG


class WordCloudGenerator:
    """
    Generates various types of word clouds for social media analytics.
    
    Types:
        - Basic word cloud from text
        - Frequency-based word cloud
        - Sentiment-colored word cloud
        - Hashtag word cloud
        - Custom shaped word cloud
    """

    def __init__(self):
        self.stopwords = set(STOPWORDS)
        # Add social-media-specific stopwords
        self.stopwords.update([
            'rt', 'via', 'amp', 'https', 'http', 'co',
            'will', 'one', 'us', 'new', 'get', 'like',
            'make', 'know', 'say', 'see', 'go', 'come',
            'take', 'use', 'would', 'also', 'just', 'still',
            'even', 'thing', 'really', 'much', 'lot'
        ])

    # ──────────────────────────────────────────
    # Basic Word Cloud
    # ──────────────────────────────────────────
    def generate_basic_wordcloud(self, text, title="Word Cloud",
                                  filename="basic_wordcloud"):
        """
        Generate a basic word cloud from text.
        """
        wordcloud = WordCloud(
            width=WORDCLOUD_CONFIG['width'],
            height=WORDCLOUD_CONFIG['height'],
            max_words=WORDCLOUD_CONFIG['max_words'],
            background_color=WORDCLOUD_CONFIG['background_color'],
            colormap=WORDCLOUD_CONFIG['colormap'],
            stopwords=self.stopwords,
            min_font_size=10,
            max_font_size=150,
            random_state=42,
            collocations=False
        ).generate(text)

        # Save using matplotlib
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=20, fontweight='bold', pad=20)

        output_path = os.path.join(WORDCLOUD_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        print(f"✅ Word cloud saved: {output_path}")
        return output_path

    # ──────────────────────────────────────────
    # Frequency-based Word Cloud
    # ──────────────────────────────────────────
    def generate_frequency_wordcloud(self, word_freq, title="Keyword Frequency",
                                      filename="freq_wordcloud"):
        """
        Generate word cloud from a word frequency dictionary.
        
        Args:
            word_freq: dict like {'word': count, ...} or list of tuples
        """
        if isinstance(word_freq, list):
            word_freq = dict(word_freq)

        wordcloud = WordCloud(
            width=WORDCLOUD_CONFIG['width'],
            height=WORDCLOUD_CONFIG['height'],
            background_color='white',
            colormap='plasma',
            max_words=150,
            min_font_size=8,
            max_font_size=200,
            prefer_horizontal=0.7,
            random_state=42
        ).generate_from_frequencies(word_freq)

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=20, fontweight='bold', pad=20)

        output_path = os.path.join(WORDCLOUD_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='white')
        plt.close()
        print(f"✅ Frequency word cloud saved: {output_path}")
        return output_path

    # ──────────────────────────────────────────
    # Sentiment Word Cloud
    # ──────────────────────────────────────────
    def generate_sentiment_wordclouds(self, positive_text, negative_text,
                                       neutral_text, filename_prefix="sentiment"):
        """
        Generate separate word clouds for each sentiment category.
        """
        output_paths = {}

        # Configuration for each sentiment
        configs = {
            'positive': {
                'text': positive_text,
                'colormap': 'Greens',
                'title': '✅ Positive Sentiment Words'
            },
            'negative': {
                'text': negative_text,
                'colormap': 'Reds',
                'title': '❌ Negative Sentiment Words'
            },
            'neutral': {
                'text': neutral_text,
                'colormap': 'Blues',
                'title': '➖ Neutral Sentiment Words'
            }
        }

        fig, axes = plt.subplots(1, 3, figsize=(24, 8))

        for idx, (sentiment, config) in enumerate(configs.items()):
            if config['text'].strip():
                wc = WordCloud(
                    width=600,
                    height=400,
                    background_color='white',
                    colormap=config['colormap'],
                    stopwords=self.stopwords,
                    max_words=100,
                    random_state=42
                ).generate(config['text'])

                axes[idx].imshow(wc, interpolation='bilinear')
            else:
                axes[idx].text(
                    0.5, 0.5, 'No data',
                    ha='center', va='center', fontsize=20
                )

            axes[idx].axis('off')
            axes[idx].set_title(config['title'], fontsize=16, fontweight='bold')

        plt.suptitle('Sentiment Word Clouds', fontsize=22, fontweight='bold', y=1.02)
        plt.tight_layout()

        output_path = os.path.join(WORDCLOUD_DIR, f"{filename_prefix}_combined.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        output_paths['combined'] = output_path
        print(f"✅ Sentiment word clouds saved: {output_path}")
        return output_paths

    # ──────────────────────────────────────────
    # Hashtag Word Cloud
    # ──────────────────────────────────────────
    def generate_hashtag_cloud(self, hashtags, title="Trending Hashtags",
                                filename="hashtag_cloud"):
        """
        Generate a word cloud from hashtag frequency.
        
        Args:
            hashtags: list of hashtags or dict of {hashtag: count}
        """
        if isinstance(hashtags, list):
            hashtag_freq = Counter(hashtags)
        else:
            hashtag_freq = hashtags

        if not hashtag_freq:
            print("⚠️  No hashtags to display")
            return None

        wordcloud = WordCloud(
            width=WORDCLOUD_CONFIG['width'],
            height=WORDCLOUD_CONFIG['height'],
            background_color='#1a1a2e',
            colormap='Set2',
            max_words=100,
            min_font_size=12,
            max_font_size=180,
            random_state=42
        ).generate_from_frequencies(hashtag_freq)

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=20, fontweight='bold',
                     color='white', pad=20)
        fig.patch.set_facecolor('#1a1a2e')

        output_path = os.path.join(WORDCLOUD_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='#1a1a2e')
        plt.close()
        print(f"✅ Hashtag cloud saved: {output_path}")
        return output_path

    # ──────────────────────────────────────────
    # Custom Shaped Word Cloud
    # ──────────────────────────────────────────
    def generate_shaped_wordcloud(self, text, mask_image_path,
                                   title="Shaped Word Cloud",
                                   filename="shaped_wordcloud"):
        """
        Generate a word cloud in the shape of a provided mask image.
        """
        if not os.path.exists(mask_image_path):
            print(f"⚠️  Mask image not found: {mask_image_path}")
            return self.generate_basic_wordcloud(text, title, filename)

        mask = np.array(Image.open(mask_image_path))

        wordcloud = WordCloud(
            mask=mask,
            background_color='white',
            max_words=300,
            stopwords=self.stopwords,
            contour_width=2,
            contour_color='steelblue',
            colormap='viridis',
            random_state=42
        ).generate(text)

        fig, ax = plt.subplots(figsize=(16, 10))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=20, fontweight='bold', pad=20)

        output_path = os.path.join(WORDCLOUD_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='white')
        plt.close()
        print(f"✅ Shaped word cloud saved: {output_path}")
        return output_path

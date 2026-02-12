"""
Emoji & Emoticon Analysis Module
- Detects and counts emojis in text
- Maps emojis to sentiment
- Analyzes emoji usage patterns
"""

import re
from collections import Counter
import emoji


class EmojiAnalyzer:
    """
    Analyzes emoji and emoticon usage in social media posts.
    
    Features:
        - Emoji extraction and counting
        - Emoji sentiment mapping
        - Emoticon detection (text-based like :) :( etc.)
        - Emoji frequency analysis
    """

    def __init__(self):
        # ──────────────────────────────────────
        # Emoticon to Sentiment Mapping
        # ──────────────────────────────────────
        self.emoticon_sentiments = {
            # Positive emoticons
            ':)': 'positive', ':-)': 'positive', ':D': 'positive',
            ':-D': 'positive', ';)': 'positive', ';-)': 'positive',
            ':P': 'positive', ':-P': 'positive', 'XD': 'positive',
            '<3': 'positive', ':*': 'positive', '^^': 'positive',
            '=)': 'positive', '=D': 'positive', 'B)': 'positive',

            # Negative emoticons
            ':(': 'negative', ':-(': 'negative', ":'(": 'negative',
            'D:': 'negative', '>:(': 'negative', ':/': 'negative',
            ':-/': 'negative', ':|': 'negative', ':-|': 'negative',
            '>.<': 'negative', 'T_T': 'negative', 'TT': 'negative',

            # Neutral emoticons
            ':-O': 'neutral', ':O': 'neutral', 'O_o': 'neutral',
            'o_O': 'neutral', '._.' : 'neutral'
        }

        # ──────────────────────────────────────
        # Emoji Sentiment Categories
        # ──────────────────────────────────────
        self.positive_emojis = {
            '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
            '🙂', '🙃', '😉', '😊', '😇', '🥰', '😍', '🤩',
            '😘', '😗', '😚', '😙', '🥲', '😋', '😛', '😜',
            '🤪', '😝', '👍', '👏', '🎉', '🎊', '❤️', '💕',
            '💖', '💗', '💓', '💝', '💘', '🌟', '⭐', '✨',
            '🔥', '💪', '🤗', '🥳', '😎', '🤟', '🙌', '👌'
        }

        self.negative_emojis = {
            '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖',
            '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡',
            '🤬', '😈', '👿', '💀', '☠️', '💔', '😰', '😥',
            '😓', '🤮', '🤢', '😱', '😨', '👎', '😒', '😑',
            '😬', '🤥', '😪', '🥱', '😵', '🤕', '🤒', '💩'
        }

    # ──────────────────────────────────────────
    # Emoji Extraction
    # ──────────────────────────────────────────
    def extract_emojis(self, text):
        """Extract all emojis from text."""
        emoji_list = []
        for char in text:
            if emoji.is_emoji(char):
                emoji_list.append({
                    'emoji': char,
                    'name': emoji.demojize(char),
                    'sentiment': self._get_emoji_sentiment(char)
                })
        return emoji_list

    def extract_emoticons(self, text):
        """Extract text-based emoticons from text."""
        found_emoticons = []
        for emoticon, sentiment in self.emoticon_sentiments.items():
            if emoticon in text:
                found_emoticons.append({
                    'emoticon': emoticon,
                    'sentiment': sentiment
                })
        return found_emoticons

    # ──────────────────────────────────────────
    # Emoji Sentiment
    # ──────────────────────────────────────────
    def _get_emoji_sentiment(self, emoji_char):
        """Determine sentiment of a single emoji."""
        if emoji_char in self.positive_emojis:
            return 'positive'
        elif emoji_char in self.negative_emojis:
            return 'negative'
        return 'neutral'

    def analyze_emoji_sentiment(self, text):
        """
        Analyze overall emoji sentiment in text.
        
        Returns:
            dict: Emoji analysis results
        """
        emojis = self.extract_emojis(text)
        emoticons = self.extract_emoticons(text)

        all_sentiments = (
            [e['sentiment'] for e in emojis] +
            [e['sentiment'] for e in emoticons]
        )

        sentiment_counts = Counter(all_sentiments)
        total = len(all_sentiments)

        if total == 0:
            overall = 'no_emoji'
            score = 0.0
        else:
            pos = sentiment_counts.get('positive', 0)
            neg = sentiment_counts.get('negative', 0)
            score = (pos - neg) / total

            if score > 0.1:
                overall = 'positive'
            elif score < -0.1:
                overall = 'negative'
            else:
                overall = 'neutral'

        return {
            'text': text,
            'emojis_found': emojis,
            'emoticons_found': emoticons,
            'total_emoji_count': len(emojis),
            'total_emoticon_count': len(emoticons),
            'sentiment_distribution': dict(sentiment_counts),
            'emoji_sentiment_score': score,
            'overall_emoji_sentiment': overall,
            'emoji_frequency': Counter([e['emoji'] for e in emojis])
        }

    # ──────────────────────────────────────────
    # Batch Analysis
    # ──────────────────────────────────────────
    def analyze_batch(self, texts):
        """Analyze emojis across multiple posts."""
        all_emojis = Counter()
        all_sentiments = Counter()
        results = []

        for text in texts:
            result = self.analyze_emoji_sentiment(text)
            results.append(result)
            all_emojis.update(result['emoji_frequency'])
            all_sentiments.update(result['sentiment_distribution'])

        return {
            'individual_results': results,
            'top_emojis': all_emojis.most_common(20),
            'overall_sentiment_distribution': dict(all_sentiments),
            'total_posts_with_emojis': sum(
                1 for r in results if r['total_emoji_count'] > 0
            )
        }

    def get_emoji_text(self, text):
        """Convert emojis to their text descriptions."""
        return emoji.demojize(text, delimiters=(" [", "] "))
"""
Chart Generation Module using Pygal and Matplotlib
- Sentiment distribution charts
- Trend analysis charts
- Engagement metrics charts
- Comparison charts
"""

import os
import pygal
from pygal.style import Style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from config import CHARTS_DIR


class ChartGenerator:
    """
    Generates business analytics charts for social media data.
    
    Chart Types:
        - Pie charts (sentiment distribution)
        - Bar charts (comparison metrics)
        - Line charts (trends over time)
        - Gauge charts (sentiment scores)
        - Radar charts (multi-metric analysis)
    """

    def __init__(self):
        # ──────────────────────────────────────
        # Custom Pygal Style
        # ──────────────────────────────────────
        self.custom_style = Style(
            background='white',
            plot_background='white',
            foreground='#333333',
            foreground_strong='#000000',
            foreground_subtle='#666666',
            colors=(
                '#2ecc71',  # Green (Positive)
                '#e74c3c',  # Red (Negative)
                '#f39c12',  # Orange (Neutral)
                '#3498db',  # Blue
                '#9b59b6',  # Purple
                '#1abc9c',  # Teal
                '#e67e22',  # Dark Orange
                '#34495e',  # Dark Gray
            ),
            font_family='Arial',
            title_font_size=20,
            label_font_size=12,
            legend_font_size=14
        )

        # Matplotlib style
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12

    # ══════════════════════════════════════════
    # PYGAL CHARTS
    # ══════════════════════════════════════════

    def sentiment_pie_chart(self, sentiment_data, title="Sentiment Distribution",
                            filename="sentiment_pie"):
        """
        Create a pie chart showing sentiment distribution.
        
        Args:
            sentiment_data: dict with keys 'positive', 'negative', 'neutral' and counts
        """
        pie_chart = pygal.Pie(style=self.custom_style)
        pie_chart.title = title

        pie_chart.add(
            f"Positive ({sentiment_data.get('positive', 0)})",
            sentiment_data.get('positive', 0)
        )
        pie_chart.add(
            f"Negative ({sentiment_data.get('negative', 0)})",
            sentiment_data.get('negative', 0)
        )
        pie_chart.add(
            f"Neutral ({sentiment_data.get('neutral', 0)})",
            sentiment_data.get('neutral', 0)
        )

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        pie_chart.render_to_file(output_path)
        print(f"✅ Pie chart saved: {output_path}")
        return output_path

    def sentiment_bar_chart(self, categories, scores, title="Sentiment Scores",
                            filename="sentiment_bar"):
        """
        Create a bar chart comparing sentiment scores across categories.
        """
        bar_chart = pygal.Bar(style=self.custom_style)
        bar_chart.title = title
        bar_chart.x_labels = categories

        # Separate positive and negative
        positive_scores = [max(s, 0) for s in scores]
        negative_scores = [min(s, 0) for s in scores]

        bar_chart.add('Positive', positive_scores)
        bar_chart.add('Negative', negative_scores)

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        bar_chart.render_to_file(output_path)
        print(f"✅ Bar chart saved: {output_path}")
        return output_path

    def sentiment_trend_line(self, timestamps, scores, title="Sentiment Trend",
                              filename="sentiment_trend"):
        """
        Create a line chart showing sentiment trend over time.
        """
        line_chart = pygal.Line(
            style=self.custom_style,
            x_label_rotation=45,
            show_minor_x_labels=False
        )
        line_chart.title = title
        line_chart.x_labels = timestamps
        line_chart.add('Sentiment Score', scores)

        # Add reference lines
        line_chart.add('Positive Threshold', [0.05] * len(timestamps))
        line_chart.add('Negative Threshold', [-0.05] * len(timestamps))

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        line_chart.render_to_file(output_path)
        print(f"✅ Line chart saved: {output_path}")
        return output_path

    def gauge_chart(self, score, title="Overall Sentiment", filename="sentiment_gauge"):
        """
        Create a gauge chart for overall sentiment score.
        """
        gauge = pygal.SolidGauge(
            style=self.custom_style,
            inner_radius=0.70,
            half_pie=True
        )
        gauge.title = title

        # Normalize score from [-1,1] to [0,100]
        normalized = (score + 1) * 50
        gauge.add('Sentiment', [{'value': round(normalized, 1), 'max_value': 100}])

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        gauge.render_to_file(output_path)
        print(f"✅ Gauge chart saved: {output_path}")
        return output_path

    def radar_chart(self, metrics, title="Multi-Metric Analysis",
                    filename="radar_analysis"):
        """
        Create a radar chart for multi-dimensional analysis.
        
        Args:
            metrics: dict of {'metric_name': {'Category1': val, 'Category2': val, ...}}
        """
        radar = pygal.Radar(style=self.custom_style)
        radar.title = title

        # Set labels from first metric's keys
        first_metric = list(metrics.values())[0]
        radar.x_labels = list(first_metric.keys())

        for name, values in metrics.items():
            radar.add(name, list(values.values()))

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        radar.render_to_file(output_path)
        print(f"✅ Radar chart saved: {output_path}")
        return output_path

    def horizontal_bar(self, labels, values, title="Top Keywords",
                       filename="top_keywords"):
        """
        Create a horizontal bar chart (e.g., for keyword frequency).
        """
        h_bar = pygal.HorizontalBar(style=self.custom_style)
        h_bar.title = title

        for label, value in zip(labels, values):
            h_bar.add(label, value)

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        h_bar.render_to_file(output_path)
        print(f"✅ Horizontal bar chart saved: {output_path}")
        return output_path

    def emoji_bar_chart(self, emoji_data, title="Top Emojis Used",
                        filename="emoji_chart"):
        """
        Create a bar chart for emoji frequency.
        """
        bar_chart = pygal.Bar(
            style=self.custom_style,
            x_label_rotation=0
        )
        bar_chart.title = title

        emojis = [item[0] for item in emoji_data]
        counts = [item[1] for item in emoji_data]

        bar_chart.x_labels = emojis
        bar_chart.add('Count', counts)

        output_path = os.path.join(CHARTS_DIR, f"{filename}.svg")
        bar_chart.render_to_file(output_path)
        print(f"✅ Emoji chart saved: {output_path}")
        return output_path

    # ══════════════════════════════════════════
    # MATPLOTLIB / SEABORN CHARTS
    # ══════════════════════════════════════════

    def matplotlib_sentiment_distribution(self, df, filename="mpl_sentiment_dist"):
        """
        Create a detailed sentiment distribution chart using Matplotlib.
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        # ── Left: Histogram of sentiment scores ──
        colors_map = {
            'Positive': '#2ecc71',
            'Negative': '#e74c3c',
            'Neutral': '#f39c12'
        }

        for label in ['Positive', 'Negative', 'Neutral']:
            subset = df[df['label'] == label]['combined_score']
            if not subset.empty:
                axes[0].hist(
                    subset, bins=20, alpha=0.7,
                    label=label, color=colors_map[label]
                )

        axes[0].set_xlabel('Sentiment Score', fontsize=14)
        axes[0].set_ylabel('Frequency', fontsize=14)
        axes[0].set_title('Sentiment Score Distribution', fontsize=16)
        axes[0].legend(fontsize=12)
        axes[0].axvline(x=0, color='gray', linestyle='--', alpha=0.5)

        # ── Right: Pie chart ──
        label_counts = df['label'].value_counts()
        pie_colors = [colors_map.get(l, '#95a5a6') for l in label_counts.index]

        axes[1].pie(
            label_counts.values,
            labels=label_counts.index,
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90,
            textprops={'fontsize': 13}
        )
        axes[1].set_title('Sentiment Proportion', fontsize=16)

        plt.tight_layout()
        output_path = os.path.join(CHARTS_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ Matplotlib chart saved: {output_path}")
        return output_path

    def matplotlib_trend_chart(self, timestamps, scores, filename="mpl_trend"):
        """
        Create a sentiment trend chart with Matplotlib.
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        # Color the line segments based on sentiment
        for i in range(len(scores) - 1):
            color = '#2ecc71' if scores[i] >= 0 else '#e74c3c'
            ax.plot(
                [timestamps[i], timestamps[i + 1]],
                [scores[i], scores[i + 1]],
                color=color, linewidth=2
            )

        # Fill areas
        ax.fill_between(
            range(len(scores)), scores, 0,
            where=[s >= 0 for s in scores],
            alpha=0.3, color='#2ecc71', label='Positive'
        )
        ax.fill_between(
            range(len(scores)), scores, 0,
            where=[s < 0 for s in scores],
            alpha=0.3, color='#e74c3c', label='Negative'
        )

        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time', fontsize=14)
        ax.set_ylabel('Sentiment Score', fontsize=14)
        ax.set_title('Sentiment Trend Over Time', fontsize=16)
        ax.legend(fontsize=12)

        plt.tight_layout()
        output_path = os.path.join(CHARTS_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ Trend chart saved: {output_path}")
        return output_path

    def matplotlib_heatmap(self, data_matrix, x_labels, y_labels,
                            title="Sentiment Heatmap", filename="heatmap"):
        """
        Create a heatmap for multi-dimensional analysis.
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        sns.heatmap(
            data_matrix,
            xticklabels=x_labels,
            yticklabels=y_labels,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            ax=ax
        )

        ax.set_title(title, fontsize=16)
        plt.tight_layout()

        output_path = os.path.join(CHARTS_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ Heatmap saved: {output_path}")
        return output_path

    def content_type_analysis(self, content_data, filename="content_types"):
        """
        Create a chart showing sentiment across different content types.
        
        Args:
            content_data: dict like {'text': 0.3, 'image': 0.5, 'video': -0.1, 'audio': 0.2}
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        types = list(content_data.keys())
        scores = list(content_data.values())
        colors = ['#2ecc71' if s >= 0 else '#e74c3c' for s in scores]

        bars = ax.bar(types, scores, color=colors, edgecolor='white', linewidth=1.5)

        # Add value labels on bars
        for bar, score in zip(bars, scores):
            va = 'bottom' if score >= 0 else 'top'
            ax.text(
                bar.get_x() + bar.get_width() / 2., score,
                f'{score:.2f}', ha='center', va=va, fontsize=13, fontweight='bold'
            )

        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Content Type', fontsize=14)
        ax.set_ylabel('Average Sentiment Score', fontsize=14)
        ax.set_title('Sentiment by Content Type', fontsize=16)

        plt.tight_layout()
        output_path = os.path.join(CHARTS_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ Content type chart saved: {output_path}")
        return output_path

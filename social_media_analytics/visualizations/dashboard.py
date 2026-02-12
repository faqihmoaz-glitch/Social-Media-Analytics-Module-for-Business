"""
Dashboard Module - Combines all analytics into a comprehensive report
"""

import os
import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from config import REPORTS_DIR


class Dashboard:
    """
    Creates comprehensive analytics dashboards combining
    all analysis results.
    """

    def generate_summary_dashboard(self, summary_data, filename="dashboard"):
        """
        Generate a comprehensive visual dashboard.
        
        Args:
            summary_data: dict containing all analysis results
        """
        fig = plt.figure(figsize=(24, 16))
        gs = gridspec.GridSpec(3, 4, hspace=0.4, wspace=0.3)

        fig.suptitle(
            '📊 Social Media Analytics Dashboard',
            fontsize=24, fontweight='bold', y=0.98
        )

        # ──────────────────────────────────────
        # 1. Overall Sentiment Score (Gauge-like)
        # ──────────────────────────────────────
        ax1 = fig.add_subplot(gs[0, 0])
        score = summary_data.get('avg_sentiment', 0)
        color = '#2ecc71' if score >= 0 else '#e74c3c'

        circle = plt.Circle((0.5, 0.5), 0.4, fill=False,
                             linewidth=8, color=color)
        ax1.add_patch(circle)
        ax1.text(0.5, 0.55, f'{score:.3f}', ha='center', va='center',
                 fontsize=28, fontweight='bold', color=color)
        ax1.text(0.5, 0.35, 'Avg Sentiment', ha='center', va='center',
                 fontsize=12, color='gray')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title('Overall Score', fontsize=14, fontweight='bold')

        # ──────────────────────────────────────
        # 2. Sentiment Distribution Pie
        # ──────────────────────────────────────
        ax2 = fig.add_subplot(gs[0, 1])
        labels = ['Positive', 'Negative', 'Neutral']
        sizes = [
            summary_data.get('positive_percentage', 33),
            summary_data.get('negative_percentage', 33),
            summary_data.get('neutral_percentage', 34)
        ]
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        explode = (0.05, 0.05, 0.05)

        ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90,
                textprops={'fontsize': 11})
        ax2.set_title('Sentiment Split', fontsize=14, fontweight='bold')

        # ──────────────────────────────────────
        # 3. Key Metrics Cards
        # ──────────────────────────────────────
        ax3 = fig.add_subplot(gs[0, 2:])
        ax3.axis('off')

        metrics = [
            ('Total Posts', summary_data.get('total_posts', 0), '#3498db'),
            ('Positive', summary_data.get('positive_count', 0), '#2ecc71'),
            ('Negative', summary_data.get('negative_count', 0), '#e74c3c'),
            ('Neutral', summary_data.get('neutral_count', 0), '#f39c12'),
        ]

        for i, (label, value, color) in enumerate(metrics):
            x = 0.1 + i * 0.23
            rect = plt.Rectangle((x, 0.2), 0.2, 0.6, linewidth=2,
                                  edgecolor=color, facecolor=color, alpha=0.15)
            ax3.add_patch(rect)
            ax3.text(x + 0.1, 0.6, str(value), ha='center', va='center',
                     fontsize=24, fontweight='bold', color=color)
            ax3.text(x + 0.1, 0.35, label, ha='center', va='center',
                     fontsize=12, color='gray')

        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.set_title('Key Metrics', fontsize=14, fontweight='bold')

        # ──────────────────────────────────────
        # 4. Content Type Sentiment
        # ──────────────────────────────────────
        ax4 = fig.add_subplot(gs[1, :2])
        content_types = summary_data.get('content_type_sentiments', {
            'Text': 0.3, 'Image': 0.5, 'Video': 0.1, 'Audio': 0.2, 'Emoji': 0.6
        })
        types = list(content_types.keys())
        values = list(content_types.values())
        bar_colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in values]

        bars = ax4.bar(types, values, color=bar_colors, edgecolor='white', linewidth=1.5)
        ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax4.set_title('Sentiment by Content Type', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Sentiment Score')

        for bar, val in zip(bars, values):
            va_pos = 'bottom' if val >= 0 else 'top'
            ax4.text(bar.get_x() + bar.get_width() / 2., val,
                     f'{val:.2f}', ha='center', va=va_pos, fontweight='bold')

        # ──────────────────────────────────────
        # 5. Emoji Distribution
        # ──────────────────────────────────────
        ax5 = fig.add_subplot(gs[1, 2:])
        emoji_data = summary_data.get('top_emojis', [
            ('😀', 45), ('❤️', 38), ('👍', 32), ('😂', 28),
            ('🔥', 22), ('😢', 15), ('😡', 10), ('🎉', 8)
        ])
        if emoji_data:
            emojis = [e[0] for e in emoji_data[:8]]
            counts = [e[1] for e in emoji_data[:8]]
            ax5.barh(emojis, counts, color='#9b59b6', edgecolor='white')
            ax5.set_title('Top Emojis', fontsize=14, fontweight='bold')
            ax5.set_xlabel('Count')
        else:
            ax5.text(0.5, 0.5, 'No emoji data', ha='center', va='center')
            ax5.axis('off')

        # ──────────────────────────────────────
        # 6. Insights Text
        # ──────────────────────────────────────
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis('off')

        insights_text = self._generate_insights(summary_data)
        ax6.text(
            0.05, 0.9, '📋 Key Insights:',
            fontsize=16, fontweight='bold', va='top',
            transform=ax6.transAxes
        )
        ax6.text(
            0.05, 0.75, insights_text,
            fontsize=12, va='top', wrap=True,
            transform=ax6.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                      alpha=0.8, edgecolor='orange')
        )

        # ── Timestamp ──
        fig.text(
            0.99, 0.01,
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            ha='right', fontsize=10, color='gray'
        )

        output_path = os.path.join(REPORTS_DIR, f"{filename}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        print(f"✅ Dashboard saved: {output_path}")
        return output_path

    def _generate_insights(self, data):
        """Generate text insights from analysis data."""
        insights = []

        avg = data.get('avg_sentiment', 0)
        if avg > 0.2:
            insights.append("• Very positive overall sentiment — brand perception is strong.")
        elif avg > 0:
            insights.append("• Slightly positive sentiment — room for improvement.")
        elif avg > -0.2:
            insights.append("• Slightly negative sentiment — attention needed.")
        else:
            insights.append("• Strongly negative sentiment — immediate action required!")

        pos_pct = data.get('positive_percentage', 0)
        neg_pct = data.get('negative_percentage', 0)

        if pos_pct > 60:
            insights.append(f"• {pos_pct:.1f}% positive posts — excellent engagement.")
        if neg_pct > 30:
            insights.append(f"• ⚠️  {neg_pct:.1f}% negative posts — investigate root causes.")

        total = data.get('total_posts', 0)
        insights.append(f"• Analyzed {total} posts across text, image, audio, video & emoji content.")

        return '\n'.join(insights)

    def generate_json_report(self, all_results, filename="full_report"):
        """Save complete analysis as JSON report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'results': self._make_serializable(all_results)
        }

        output_path = os.path.join(REPORTS_DIR, f"{filename}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ JSON report saved: {output_path}")
        return output_path

    def _make_serializable(self, obj):
        """Recursively make objects JSON-serializable."""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(i) for i in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

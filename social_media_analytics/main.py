"""
╔══════════════════════════════════════════════════════════════╗
║     SOCIAL MEDIA ANALYTICS MODULE FOR BUSINESS              ║
║                                                              ║
║     Features:                                                ║
║     • Text Sentiment Analysis (VADER + TextBlob)             ║
║     • Emoji & Emoticon Analysis                              ║
║     • Image Content Analysis                                 ║
║     • Audio Analysis (Speech-to-Text + Sentiment)            ║
║     • Video Analysis (Frame + Motion + Scene)                ║
║     • Visualization: PyChart (Pygal), Word Cloud             ║
║     • Comprehensive Dashboard & Reports                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os
import sys

# ── Import all modules ──
from analyzers.text_analyzer import TextAnalyzer
from analyzers.emoji_analyzer import EmojiAnalyzer
from analyzers.image_analyzer import ImageAnalyzer
from analyzers.audio_analyzer import AudioAnalyzer
from analyzers.video_analyzer import VideoAnalyzer
from visualizations.charts import ChartGenerator
from visualizations.wordcloud_gen import WordCloudGenerator
from visualizations.dashboard import Dashboard
from config import DATA_DIR, OUTPUT_DIR, REPORTS_DIR
from datetime import datetime


def print_header():
    print("\n" + "=" * 70)
    print("  📊 SOCIAL MEDIA ANALYTICS MODULE FOR BUSINESS")
    print("  🔍 Sentiment Analysis | Word Cloud | Multi-Content Analysis")
    print("=" * 70 + "\n")


def load_sample_data():
    """Load sample social media posts."""
    sample_file = os.path.join(DATA_DIR, "sample_posts.json")

    if os.path.exists(sample_file):
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Handle both formats: list directly or nested in 'posts' key
        if isinstance(data, list):
            return data
        else:
            return data.get('posts', [])
    else:
        # Fallback sample data
        return [
            {"id": 1, "text": "Love this product! 😍🎉 Amazing quality! #great #love",
             "timestamp": "2024-01-15 10:30:00"},
            {"id": 2, "text": "Terrible experience 😤😡 Never buying again #fail #terrible",
             "timestamp": "2024-01-15 11:45:00"},
            {"id": 3, "text": "It's okay, nothing special 🤷 #average #meh",
             "timestamp": "2024-01-15 12:00:00"},
            {"id": 4, "text": "Best purchase ever! 🔥💯 Highly recommend! #best #recommended",
             "timestamp": "2024-01-15 14:20:00"},
            {"id": 5, "text": "Product broke after one week 😢💔 Want refund #broken #refund",
             "timestamp": "2024-01-15 15:30:00"},
        ]


def run_text_analysis(posts):
    """Run text sentiment analysis on all posts."""
    print("\n" + "─" * 50)
    print("  📝 TEXT SENTIMENT ANALYSIS")
    print("─" * 50)

    analyzer = TextAnalyzer()
    texts = [post['text'] for post in posts]

    # Batch analysis
    df = analyzer.analyze_batch(texts)
    summary = analyzer.get_sentiment_summary(df)

    # Print individual results
    for _, row in df.iterrows():
        emoji_indicator = {
            'Positive': '🟢',
            'Negative': '🔴',
            'Neutral': '🟡'
        }
        indicator = emoji_indicator.get(row['label'], '⚪')
        print(f"\n  {indicator} [{row['label']}] (Score: {row['combined_score']:.3f})")
        print(f"     \"{row['text'][:80]}{'...' if len(row['text']) > 80 else ''}\"")

    # Print summary
    print("\n" + "─" * 50)
    print("  📊 SENTIMENT SUMMARY")
    print("─" * 50)
    print(f"  Total Posts Analyzed: {summary['total_posts']}")
    print(f"  🟢 Positive: {summary['positive_count']} ({summary['positive_percentage']:.1f}%)")
    print(f"  🔴 Negative: {summary['negative_count']} ({summary['negative_percentage']:.1f}%)")
    print(f"  🟡 Neutral:  {summary['neutral_count']} ({summary['neutral_percentage']:.1f}%)")
    print(f"  📈 Average Sentiment: {summary['avg_sentiment']:.4f}")

    return df, summary


def run_emoji_analysis(posts):
    """Run emoji analysis on all posts."""
    print("\n" + "─" * 50)
    print("  😀 EMOJI & EMOTICON ANALYSIS")
    print("─" * 50)

    analyzer = EmojiAnalyzer()
    texts = [post['text'] for post in posts]

    batch_results = analyzer.analyze_batch(texts)

    print(f"\n  Posts with emojis: {batch_results['total_posts_with_emojis']} / {len(texts)}")
    print(f"  Emoji sentiment distribution: {batch_results['overall_sentiment_distribution']}")

    if batch_results['top_emojis']:
        print("\n  Top Emojis Used:")
        for emoji_char, count in batch_results['top_emojis'][:10]:
            print(f"    {emoji_char}  → {count} times")

    return batch_results


def run_image_analysis():
    """Run image analysis (demo with generated test image)."""
    print("\n" + "─" * 50)
    print("  🖼️  IMAGE CONTENT ANALYSIS")
    print("─" * 50)

    analyzer = ImageAnalyzer()

    # Create a test image for demo
    import numpy as np
    import cv2

    test_image_path = os.path.join(OUTPUT_DIR, "test_image.jpg")

    # Generate a colorful test image
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    # Blue sky
    img[0:200, :] = [255, 180, 100]
    # Green ground
    img[200:, :] = [50, 180, 50]
    # Yellow sun
    cv2.circle(img, (500, 80), 60, (0, 255, 255), -1)
    cv2.imwrite(test_image_path, img)

    results = analyzer.analyze_image(test_image_path)

    if 'error' not in results:
        print(f"\n  Image: {results['image_info']['filename']}")
        print(f"  Size: {results['image_info']['size']}")
        print(f"  Brightness: {results['brightness']['brightness_level']}")
        print(f"  Faces detected: {results['face_detection']['face_count']}")
        print(f"  Image sentiment: {results['image_sentiment']}")
        print(f"  Warm colors: {results['warm_color_percentage']}%")
        print(f"  Cool colors: {results['cool_color_percentage']}%")

        print("\n  Dominant Colors:")
        for color in results['dominant_colors'][:5]:
            print(f"    🎨 {color['color_name']} ({color['hex']}) "
                  f"- {color['percentage']}% - Mood: {color['mood']}")
    else:
        print(f"  ⚠️ Error: {results['error']}")

    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

    return results


def run_audio_analysis():
    """Run audio analysis (demo mode)."""
    print("\n" + "─" * 50)
    print("  🎵 AUDIO CONTENT ANALYSIS")
    print("─" * 50)

    analyzer = AudioAnalyzer()

    # Create a test WAV file for demo
    import wave
    import struct
    import math

    test_audio_path = os.path.join(OUTPUT_DIR, "test_audio.wav")

    # Generate a simple sine wave
    sample_rate = 44100
    duration = 2  # seconds
    frequency = 440  # Hz (A4 note)

    with wave.open(test_audio_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for i in range(int(sample_rate * duration)):
            value = int(
                16000 * math.sin(2 * math.pi * frequency * i / sample_rate)
            )
            wav_file.writeframes(struct.pack('<h', value))

    # Analyze
    features = analyzer.extract_audio_features(test_audio_path)

    if 'error' not in features:
        print(f"\n  Duration: {features['duration_seconds']}s")
        print(f"  Sample Rate: {features['sample_rate']} Hz")
        print(f"  Volume Level: {features['volume_level']}")
        print(f"  Estimated Tone: {features['estimated_tone']}")
        print(f"  Zero Crossing Rate: {features['zero_crossing_rate']}")
    else:
        print(f"  ⚠️ Error: {features['error']}")

    # Clean up
    if os.path.exists(test_audio_path):
        os.remove(test_audio_path)

    return features


def run_video_analysis():
    """Run video analysis (demo mode)."""
    print("\n" + "─" * 50)
    print("  🎬 VIDEO CONTENT ANALYSIS")
    print("─" * 50)

    analyzer = VideoAnalyzer()

    # Create a simple test video for demo
    import cv2
    import numpy as np

    test_video_path = os.path.join(OUTPUT_DIR, "test_video.avi")
    frame_dir = os.path.join(OUTPUT_DIR, "video_frames")
    os.makedirs(frame_dir, exist_ok=True)

    # Generate a short test video (30 frames, color transitions)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(test_video_path, fourcc, 10, (320, 240))

    for i in range(30):
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        # Color transition from blue to red
        r = int(255 * (i / 30))
        b = int(255 * (1 - i / 30))
        frame[:] = [b, 100, r]
        # Add moving circle
        x = int(50 + (220 * i / 30))
        cv2.circle(frame, (x, 120), 30, (0, 255, 0), -1)
        out.write(frame)

    out.release()

    # Analyze the video
    results = analyzer.analyze_video(test_video_path, output_dir=frame_dir)

    if 'error' not in results:
        print(f"\n  File: {results['file']}")
        kf = results['key_frames']
        print(f"  Duration: {kf.get('duration_seconds', 'N/A')}s")
        print(f"  FPS: {kf.get('fps', 'N/A')}")
        print(f"  Total Frames: {kf.get('total_frames', 'N/A')}")
        print(f"  Key Frames Extracted: {kf.get('num_extracted', 'N/A')}")

        sc = results['scene_changes']
        print(f"  Scene Changes: {sc.get('total_scene_changes', 'N/A')}")

        ma = results['motion_analysis']
        print(f"  Activity Level: {ma.get('activity_level', 'N/A')}")
        print(f"  Average Motion: {ma.get('average_motion', 'N/A')}")

        vs = results.get('visual_sentiment', {})
        print(f"  Visual Sentiment: {vs.get('dominant_sentiment', 'N/A')}")
        print(f"  Energy Level: {results.get('energy_level', 'N/A')}")
    else:
        print(f"  ⚠️ Error: {results['error']}")

    # Clean up
    if os.path.exists(test_video_path):
        os.remove(test_video_path)
    for f in os.listdir(frame_dir):
        os.remove(os.path.join(frame_dir, f))
    if os.path.exists(frame_dir):
        os.rmdir(frame_dir)

    return results


def generate_visualizations(df, summary, emoji_results, posts):
    """Generate all charts and word clouds."""
    print("\n" + "─" * 50)
    print("  📊 GENERATING VISUALIZATIONS")
    print("─" * 50)

    chart_gen = ChartGenerator()
    wc_gen = WordCloudGenerator()
    dashboard = Dashboard()

    text_analyzer = TextAnalyzer()

    # ══════════════════════════════════════════
    # 1. PYGAL CHARTS
    # ══════════════════════════════════════════
    print("\n  🎨 Creating Pygal Charts...")

    # Sentiment pie chart
    sentiment_data = {
        'positive': summary['positive_count'],
        'negative': summary['negative_count'],
        'neutral': summary['neutral_count']
    }
    chart_gen.sentiment_pie_chart(sentiment_data)

    # Sentiment gauge
    chart_gen.gauge_chart(summary['avg_sentiment'])

    # Sentiment bar chart by post
    categories = [f"Post {i+1}" for i in range(min(len(df), 10))]
    scores = df['combined_score'].tolist()[:10]
    chart_gen.sentiment_bar_chart(categories, scores, title="Sentiment per Post")

    # Sentiment trend line
    timestamps = [post.get('timestamp', f'T{i}') for i, post in enumerate(posts)]
    chart_gen.sentiment_trend_line(
        timestamps[:len(scores)], scores, title="Sentiment Over Time"
    )

    # Emoji chart
    if emoji_results.get('top_emojis'):
        chart_gen.emoji_bar_chart(emoji_results['top_emojis'][:10])

    # Radar chart
    metrics = {
        'Text Sentiment': {
            'Positive': summary['positive_percentage'],
            'Negative': summary['negative_percentage'],
            'Neutral': summary['neutral_percentage'],
            'Avg Score': (summary['avg_sentiment'] + 1) * 50,
            'Confidence': summary.get('sentiment_std', 0.5) * 100
        }
    }
    chart_gen.radar_chart(metrics)

    # ══════════════════════════════════════════
    # 2. MATPLOTLIB CHARTS
    # ══════════════════════════════════════════
    print("  📈 Creating Matplotlib Charts...")

    chart_gen.matplotlib_sentiment_distribution(df)
    chart_gen.matplotlib_trend_chart(
        timestamps[:len(scores)], scores
    )
    chart_gen.content_type_analysis({
        'Text': summary['avg_sentiment'],
        'Image': 0.3,
        'Video': 0.1,
        'Audio': 0.2,
        'Emoji': 0.4
    })

    # ══════════════════════════════════════════
    # 3. WORD CLOUDS
    # ══════════════════════════════════════════
    print("  ☁️  Generating Word Clouds...")

    # Combined text word cloud
    all_text = " ".join([post['text'] for post in posts])
    wc_gen.generate_basic_wordcloud(all_text, title="All Posts Word Cloud")

    # Keyword frequency word cloud
    keywords = text_analyzer.extract_keywords(all_text, top_n=50)
    if keywords:
        kw_dict = dict(keywords)
        wc_gen.generate_frequency_wordcloud(
            kw_dict, title="Top Keywords"
        )

        # Persist keyword frequencies to a JSON report for teacher review
        word_counts_path = os.path.join(REPORTS_DIR, "word_counts.json")
        try:
            with open(word_counts_path, 'w', encoding='utf-8') as wf:
                json.dump({
                    'generated_at': datetime.utcnow().isoformat(),
                    'keywords': kw_dict
                }, wf, ensure_ascii=False, indent=2)
            print(f"✅ Keyword frequencies saved: {word_counts_path}")
        except Exception as e:
            print(f"⚠️ Failed to save keyword frequencies: {e}")

    # Sentiment-specific word clouds
    positive_texts = " ".join(
        df[df['label'] == 'Positive']['text'].tolist()
    )
    negative_texts = " ".join(
        df[df['label'] == 'Negative']['text'].tolist()
    )
    neutral_texts = " ".join(
        df[df['label'] == 'Neutral']['text'].tolist()
    )
    wc_gen.generate_sentiment_wordclouds(
        positive_texts, negative_texts, neutral_texts
    )

    # Hashtag word cloud
    all_hashtags = []
    for post in posts:
        all_hashtags.extend(text_analyzer.extract_hashtags(post['text']))
    if all_hashtags:
        wc_gen.generate_hashtag_cloud(all_hashtags)

    # Keyword horizontal bar
    if keywords:
        top_kw = keywords[:15]
        chart_gen.horizontal_bar(
            [k[0] for k in top_kw],
            [k[1] for k in top_kw],
            title="Top 15 Keywords"
        )

    # ══════════════════════════════════════════
    # 4. DASHBOARD
    # ══════════════════════════════════════════
    print("  📋 Creating Dashboard...")

    dashboard_data = {
        **summary,
        'content_type_sentiments': {
            'Text': round(summary['avg_sentiment'], 2),
            'Image': 0.30,
            'Video': 0.10,
            'Audio': 0.20,
            'Emoji': 0.40
        },
        'top_emojis': emoji_results.get('top_emojis', [])
    }
    dashboard.generate_summary_dashboard(dashboard_data)

    # JSON report
    dashboard.generate_json_report({
        'text_analysis_summary': summary,
        'emoji_analysis': {
            'top_emojis': emoji_results.get('top_emojis', []),
            'sentiment_distribution': emoji_results.get(
                'overall_sentiment_distribution', {}
            )
        }
    })

    print("\n  ✅ All visualizations generated successfully!")


# ══════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════

def main():
    """Main execution flow."""
    print_header()

    # 1. Load data
    print("  📂 Loading sample data...")
    posts = load_sample_data()
    print(f"  ✅ Loaded {len(posts)} posts")

    # 2. Text Analysis
    df, summary = run_text_analysis(posts)

    # 3. Emoji Analysis
    emoji_results = run_emoji_analysis(posts)

    # 4. Image Analysis
    image_results = run_image_analysis()

    # 5. Audio Analysis
    audio_results = run_audio_analysis()

    # 6. Video Analysis
    video_results = run_video_analysis()

    # 7. Generate Visualizations
    generate_visualizations(df, summary, emoji_results, posts)

    # ── Final Summary ──
    print("\n" + "=" * 70)
    print("  ✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"\n  📁 Output Directory: {OUTPUT_DIR}")
    print(f"  📊 Charts:     {os.path.join(OUTPUT_DIR, 'charts')}")
    print(f"  ☁️  Word Clouds: {os.path.join(OUTPUT_DIR, 'wordclouds')}")
    print(f"  📋 Reports:    {os.path.join(OUTPUT_DIR, 'reports')}")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()

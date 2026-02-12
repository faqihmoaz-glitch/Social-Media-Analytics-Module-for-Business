"""
Image Content Analysis Module
- OCR text extraction from images
- Image sentiment (color analysis)
- Object detection (basic)
- Logo/Brand detection
"""

import os
import cv2
import numpy as np
from PIL import Image
from collections import Counter


class ImageAnalyzer:
    """
    Analyzes images from social media posts.
    
    Features:
        - Color analysis and dominant color extraction
        - Brightness and contrast analysis
        - Color-based mood/sentiment estimation
        - Basic face detection
        - Image metadata extraction
    """

    def __init__(self):
        # ──────────────────────────────────────
        # Color-to-Mood Mapping
        # ──────────────────────────────────────
        self.color_mood_map = {
            'red': 'energetic/passionate',
            'orange': 'enthusiastic/warm',
            'yellow': 'happy/optimistic',
            'green': 'calm/natural',
            'blue': 'trustworthy/calm',
            'purple': 'creative/luxurious',
            'pink': 'romantic/playful',
            'black': 'sophisticated/serious',
            'white': 'clean/minimal',
            'gray': 'neutral/professional',
            'brown': 'earthy/reliable'
        }

        # Load face detection cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    # ──────────────────────────────────────────
    # Color Analysis
    # ──────────────────────────────────────────
    def get_dominant_colors(self, image_path, n_colors=5):
        """
        Extract dominant colors from an image using K-means clustering.
        """
        image = cv2.imread(image_path)
        if image is None:
            return {'error': 'Could not load image'}

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (150, 150))  # Resize for speed

        # Reshape to list of pixels
        pixels = image.reshape(-1, 3).astype(np.float32)

        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(
            pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )

        # Count pixels in each cluster
        label_counts = Counter(labels.flatten())
        total_pixels = len(labels)

        dominant_colors = []
        for idx, center in enumerate(centers):
            color_rgb = tuple(int(c) for c in center)
            percentage = (label_counts[idx] / total_pixels) * 100
            color_name = self._rgb_to_color_name(color_rgb)

            dominant_colors.append({
                'rgb': color_rgb,
                'hex': '#{:02x}{:02x}{:02x}'.format(*color_rgb),
                'color_name': color_name,
                'percentage': round(percentage, 2),
                'mood': self.color_mood_map.get(color_name, 'undefined')
            })

        # Sort by percentage
        dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
        return dominant_colors

    def _rgb_to_color_name(self, rgb):
        """Convert RGB tuple to approximate color name."""
        r, g, b = rgb

        if r > 200 and g > 200 and b > 200:
            return 'white'
        elif r < 50 and g < 50 and b < 50:
            return 'black'
        elif r > 150 and g < 100 and b < 100:
            return 'red'
        elif r > 200 and g > 150 and b < 100:
            return 'orange'
        elif r > 200 and g > 200 and b < 100:
            return 'yellow'
        elif r < 100 and g > 150 and b < 100:
            return 'green'
        elif r < 100 and g < 100 and b > 150:
            return 'blue'
        elif r > 150 and g < 100 and b > 150:
            return 'purple'
        elif r > 200 and g > 100 and b > 150:
            return 'pink'
        elif 100 < r < 200 and 100 < g < 200 and 100 < b < 200:
            return 'gray'
        elif r > 150 and g > 100 and b < 80:
            return 'brown'
        else:
            return 'mixed'

    # ──────────────────────────────────────────
    # Image Properties
    # ──────────────────────────────────────────
    def analyze_brightness(self, image_path):
        """Analyze image brightness level."""
        image = cv2.imread(image_path)
        if image is None:
            return {'error': 'Could not load image'}

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        brightness = np.mean(hsv[:, :, 2])

        if brightness > 170:
            level = 'very_bright'
        elif brightness > 120:
            level = 'bright'
        elif brightness > 80:
            level = 'moderate'
        elif brightness > 40:
            level = 'dark'
        else:
            level = 'very_dark'

        return {
            'brightness_value': float(brightness),
            'brightness_level': level,
            'mood_suggestion': 'positive/energetic' if brightness > 120 else 'moody/dramatic'
        }

    # ──────────────────────────────────────────
    # Face Detection
    # ──────────────────────────────────────────
    def detect_faces(self, image_path):
        """Detect faces in the image."""
        image = cv2.imread(image_path)
        if image is None:
            return {'error': 'Could not load image'}

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        face_data = []
        for (x, y, w, h) in faces:
            face_data.append({
                'position': {'x': int(x), 'y': int(y)},
                'size': {'width': int(w), 'height': int(h)}
            })

        return {
            'face_count': len(faces),
            'faces': face_data,
            'has_people': len(faces) > 0
        }

    # ──────────────────────────────────────────
    # Complete Image Analysis
    # ──────────────────────────────────────────
    def analyze_image(self, image_path):
        """
        Perform complete image analysis.
        
        Returns:
            dict: Comprehensive image analysis results
        """
        if not os.path.exists(image_path):
            return {'error': f'Image not found: {image_path}'}

        # Get image info
        img = Image.open(image_path)
        image_info = {
            'filename': os.path.basename(image_path),
            'format': img.format,
            'size': img.size,
            'mode': img.mode
        }

        results = {
            'image_info': image_info,
            'dominant_colors': self.get_dominant_colors(image_path),
            'brightness': self.analyze_brightness(image_path),
            'face_detection': self.detect_faces(image_path)
        }

        # ── Overall image sentiment ──
        colors = results['dominant_colors']
        brightness = results['brightness']

        warm_colors = sum(
            c['percentage'] for c in colors
            if c['color_name'] in ['red', 'orange', 'yellow', 'pink']
        )
        cool_colors = sum(
            c['percentage'] for c in colors
            if c['color_name'] in ['blue', 'green', 'purple']
        )

        if warm_colors > cool_colors and brightness['brightness_value'] > 120:
            image_sentiment = 'positive'
        elif cool_colors > warm_colors and brightness['brightness_value'] < 80:
            image_sentiment = 'negative'
        else:
            image_sentiment = 'neutral'

        results['image_sentiment'] = image_sentiment
        results['warm_color_percentage'] = round(warm_colors, 2)
        results['cool_color_percentage'] = round(cool_colors, 2)

        return results
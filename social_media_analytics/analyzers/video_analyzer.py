"""
Video Content Analysis Module
- Frame extraction and analysis
- Scene detection
- Audio extraction from video
- Combined video sentiment analysis
"""

import os
import cv2
import numpy as np
from analyzers.image_analyzer import ImageAnalyzer
from analyzers.audio_analyzer import AudioAnalyzer


class VideoAnalyzer:
    """
    Analyzes video content from social media.
    
    Features:
        - Key frame extraction
        - Visual sentiment per frame
        - Scene change detection
        - Motion analysis
        - Audio extraction and analysis
    """

    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        self.audio_analyzer = AudioAnalyzer()

    # ──────────────────────────────────────────
    # Frame Extraction
    # ──────────────────────────────────────────
    def extract_key_frames(self, video_path, num_frames=10, output_dir=None):
        """
        Extract evenly-spaced key frames from a video.
        """
        if not os.path.exists(video_path):
            return {'error': f'Video not found: {video_path}'}

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0

        if total_frames == 0:
            cap.release()
            return {'error': 'Could not read video frames'}

        # Calculate frame indices
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

        frames = []
        frame_paths = []

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        for i, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()

            if ret:
                timestamp = frame_idx / fps if fps > 0 else 0
                frames.append({
                    'frame_index': int(frame_idx),
                    'timestamp': round(timestamp, 2),
                    'frame_data': frame
                })

                if output_dir:
                    frame_path = os.path.join(output_dir, f'frame_{i:04d}.jpg')
                    cv2.imwrite(frame_path, frame)
                    frame_paths.append(frame_path)

        cap.release()

        return {
            'total_frames': total_frames,
            'fps': fps,
            'duration_seconds': round(duration, 2),
            'extracted_frames': frames,
            'frame_paths': frame_paths,
            'num_extracted': len(frames)
        }

    # ──────────────────────────────────────────
    # Scene Change Detection
    # ──────────────────────────────────────────
    def detect_scene_changes(self, video_path, threshold=30.0):
        """Detect scene changes based on frame difference."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {'error': 'Could not open video'}

        fps = cap.get(cv2.CAP_PROP_FPS)
        scene_changes = []
        prev_frame = None
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (320, 240))

            if prev_frame is not None:
                diff = cv2.absdiff(prev_frame, gray)
                mean_diff = np.mean(diff)

                if mean_diff > threshold:
                    timestamp = frame_idx / fps if fps > 0 else 0
                    scene_changes.append({
                        'frame_index': frame_idx,
                        'timestamp': round(timestamp, 2),
                        'difference_score': round(float(mean_diff), 2)
                    })

            prev_frame = gray
            frame_idx += 1

        cap.release()

        return {
            'total_scene_changes': len(scene_changes),
            'scene_changes': scene_changes,
            'avg_scene_duration': round(
                (frame_idx / fps) / max(len(scene_changes), 1), 2
            ) if fps > 0 else 0
        }

    # ──────────────────────────────────────────
    # Motion Analysis
    # ──────────────────────────────────────────
    def analyze_motion(self, video_path, sample_interval=5):
        """Analyze motion intensity throughout the video."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {'error': 'Could not open video'}

        fps = cap.get(cv2.CAP_PROP_FPS)
        motion_data = []
        prev_frame = None
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % sample_interval == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (320, 240))

                if prev_frame is not None:
                    diff = cv2.absdiff(prev_frame, gray)
                    motion_score = float(np.mean(diff))
                    timestamp = frame_idx / fps if fps > 0 else 0

                    motion_data.append({
                        'frame_index': frame_idx,
                        'timestamp': round(timestamp, 2),
                        'motion_score': round(motion_score, 2)
                    })

                prev_frame = gray

            frame_idx += 1

        cap.release()

        if motion_data:
            scores = [m['motion_score'] for m in motion_data]
            avg_motion = np.mean(scores)
            max_motion = np.max(scores)

            if avg_motion > 20:
                activity_level = 'high_activity'
            elif avg_motion > 8:
                activity_level = 'moderate_activity'
            else:
                activity_level = 'low_activity'
        else:
            avg_motion = 0
            max_motion = 0
            activity_level = 'unknown'

        return {
            'motion_timeline': motion_data,
            'average_motion': round(float(avg_motion), 2),
            'max_motion': round(float(max_motion), 2),
            'activity_level': activity_level
        }

    # ──────────────────────────────────────────
    # Complete Video Analysis
    # ──────────────────────────────────────────
    def analyze_video(self, video_path, output_dir=None):
        """
        Perform complete video analysis.
        
        Returns:
            dict: Comprehensive video analysis results
        """
        if not os.path.exists(video_path):
            return {'error': f'Video not found: {video_path}'}

        results = {
            'file': os.path.basename(video_path),
            'key_frames': self.extract_key_frames(
                video_path, num_frames=5, output_dir=output_dir
            ),
            'scene_changes': self.detect_scene_changes(video_path),
            'motion_analysis': self.analyze_motion(video_path)
        }

        # Analyze extracted frames for visual sentiment
        frame_sentiments = []
        for frame_path in results['key_frames'].get('frame_paths', []):
            img_analysis = self.image_analyzer.analyze_image(frame_path)
            frame_sentiments.append(img_analysis.get('image_sentiment', 'neutral'))

        if frame_sentiments:
            from collections import Counter
            sentiment_counts = Counter(frame_sentiments)
            results['visual_sentiment'] = {
                'frame_sentiments': frame_sentiments,
                'distribution': dict(sentiment_counts),
                'dominant_sentiment': sentiment_counts.most_common(1)[0][0]
            }
        else:
            results['visual_sentiment'] = {'dominant_sentiment': 'unknown'}

        # Activity-based sentiment enhancement
        activity = results['motion_analysis'].get('activity_level', 'unknown')
        if activity == 'high_activity':
            results['energy_level'] = 'high'
        elif activity == 'low_activity':
            results['energy_level'] = 'low'
        else:
            results['energy_level'] = 'moderate'

        return results
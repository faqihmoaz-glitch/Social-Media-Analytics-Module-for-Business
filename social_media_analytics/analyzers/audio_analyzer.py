"""
Audio Content Analysis Module
- Speech-to-text conversion
- Audio sentiment analysis
- Tone and pitch analysis
"""

import os
import wave
import numpy as np

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

from analyzers.text_analyzer import TextAnalyzer


class AudioAnalyzer:
    """
    Analyzes audio content from social media.
    
    Features:
        - Speech-to-text transcription
        - Sentiment analysis on transcribed text
        - Audio feature extraction (volume, pitch estimation)
        - Tone analysis
    """

    def __init__(self):
        if SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
        self.text_analyzer = TextAnalyzer()

    # ──────────────────────────────────────────
    # Speech to Text
    # ──────────────────────────────────────────
    def transcribe_audio(self, audio_path):
        """
        Convert audio file to text using Google Speech Recognition.
        """
        if not SR_AVAILABLE:
            return {
                'error': 'speech_recognition not installed',
                'transcription': ''
            }

        if not os.path.exists(audio_path):
            return {'error': f'Audio file not found: {audio_path}'}

        try:
            with sr.AudioFile(audio_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)

            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data)
            return {
                'transcription': text,
                'success': True,
                'engine': 'google'
            }
        except sr.UnknownValueError:
            return {
                'transcription': '',
                'success': False,
                'error': 'Speech not recognized'
            }
        except sr.RequestError as e:
            return {
                'transcription': '',
                'success': False,
                'error': f'API error: {str(e)}'
            }

    # ──────────────────────────────────────────
    # Audio Feature Extraction
    # ──────────────────────────────────────────
    def extract_audio_features(self, audio_path):
        """Extract basic audio features from a WAV file."""
        if not os.path.exists(audio_path):
            return {'error': f'File not found: {audio_path}'}

        try:
            with wave.open(audio_path, 'rb') as wav_file:
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                duration = n_frames / float(frame_rate)

                # Read audio data
                raw_data = wav_file.readframes(n_frames)
                if sample_width == 2:
                    audio_data = np.frombuffer(raw_data, dtype=np.int16)
                elif sample_width == 4:
                    audio_data = np.frombuffer(raw_data, dtype=np.int32)
                else:
                    audio_data = np.frombuffer(raw_data, dtype=np.uint8)

                audio_float = audio_data.astype(np.float64)

            # ── Calculate features ──
            rms = np.sqrt(np.mean(audio_float ** 2))
            max_amplitude = np.max(np.abs(audio_float))
            zero_crossings = np.sum(np.diff(np.sign(audio_float)) != 0)
            zcr = zero_crossings / len(audio_float)

            # Volume classification
            if sample_width == 2:
                max_possible = 32767
            else:
                max_possible = max_amplitude if max_amplitude > 0 else 1

            volume_ratio = rms / max_possible
            if volume_ratio > 0.3:
                volume_level = 'loud'
            elif volume_ratio > 0.1:
                volume_level = 'moderate'
            else:
                volume_level = 'quiet'

            # Energy-based tone estimate
            if zcr > 0.1 and volume_ratio > 0.2:
                tone = 'excited/energetic'
            elif zcr < 0.05 and volume_ratio < 0.1:
                tone = 'calm/subdued'
            elif volume_ratio > 0.3:
                tone = 'assertive/angry'
            else:
                tone = 'neutral/conversational'

            return {
                'duration_seconds': round(duration, 2),
                'sample_rate': frame_rate,
                'channels': n_channels,
                'rms_volume': round(float(rms), 2),
                'max_amplitude': float(max_amplitude),
                'zero_crossing_rate': round(float(zcr), 4),
                'volume_level': volume_level,
                'estimated_tone': tone
            }

        except Exception as e:
            return {'error': f'Error processing audio: {str(e)}'}

    # ──────────────────────────────────────────
    # Complete Audio Analysis
    # ──────────────────────────────────────────
    def analyze_audio(self, audio_path):
        """
        Perform complete audio analysis.
        
        Returns:
            dict: Audio features, transcription, and sentiment
        """
        results = {
            'file': os.path.basename(audio_path),
            'audio_features': self.extract_audio_features(audio_path),
            'transcription': self.transcribe_audio(audio_path)
        }

        # If transcription successful, analyze sentiment
        if results['transcription'].get('success'):
            text = results['transcription']['transcription']
            results['text_sentiment'] = self.text_analyzer.combined_sentiment(text)
        else:
            # Use audio features for sentiment estimation
            features = results['audio_features']
            if not isinstance(features, dict) or 'error' in features:
                results['audio_sentiment'] = 'unknown'
            else:
                tone = features.get('estimated_tone', '')
                if 'excited' in tone or 'energetic' in tone:
                    results['audio_sentiment'] = 'positive'
                elif 'angry' in tone:
                    results['audio_sentiment'] = 'negative'
                else:
                    results['audio_sentiment'] = 'neutral'

        return results
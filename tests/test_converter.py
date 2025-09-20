"""
Test suite for Advanced Speech-to-Text Converter
===============================================

This module contains unit tests for the core functionality
of the speech-to-text converter.
"""

import unittest
import tempfile
import os
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
import sys

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 0099 import SpeechToTextConverter


class TestSpeechToTextConverter(unittest.TestCase):
    """Test cases for SpeechToTextConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create a temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        test_config = {
            "google_api_key": "",
            "azure_key": "",
            "azure_region": "",
            "openai_api_key": "",
            "whisper_model": "base",
            "default_language": "en-US",
            "supported_languages": {
                "en-US": "English (US)",
                "es-ES": "Spanish"
            },
            "audio_settings": {
                "sample_rate": 16000,
                "channels": 1,
                "format": "wav"
            }
        }
        json.dump(test_config, self.temp_config)
        self.temp_config.close()
        
        # Initialize converter with test database
        with patch('0099.sqlite3.connect') as mock_connect:
            mock_connect.return_value = sqlite3.connect(self.temp_db.name)
            self.converter = SpeechToTextConverter(self.temp_config.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary files
        try:
            os.unlink(self.temp_db.name)
            os.unlink(self.temp_config.name)
        except OSError:
            pass
    
    def test_config_loading(self):
        """Test configuration loading."""
        self.assertEqual(self.converter.config["default_language"], "en-US")
        self.assertEqual(self.converter.config["whisper_model"], "base")
        self.assertIn("en-US", self.converter.config["supported_languages"])
    
    def test_database_initialization(self):
        """Test database initialization."""
        # Check if database file exists
        self.assertTrue(os.path.exists(self.temp_db.name))
        
        # Check if table was created
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transcriptions'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "transcriptions")
    
    def test_engine_initialization(self):
        """Test recognition engines initialization."""
        self.assertIn("google", self.converter.engines)
        self.assertIn("whisper", self.converter.engines)
        self.assertIn("azure", self.converter.engines)
        self.assertIn("openai", self.converter.engines)
    
    @patch('0099.sr.Microphone')
    @patch('0099.sr.Recognizer')
    def test_microphone_transcription_success(self, mock_recognizer_class, mock_microphone_class):
        """Test successful microphone transcription."""
        # Mock the recognizer and microphone
        mock_recognizer = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        mock_recognizer.adjust_for_ambient_noise.return_value = None
        mock_recognizer.listen.return_value = Mock()
        
        # Mock the Google recognition
        mock_recognizer.recognize_google.return_value = "Hello world"
        
        # Mock the microphone context manager
        mock_microphone = Mock()
        mock_microphone_class.return_value.__enter__.return_value = mock_microphone
        
        result = self.converter.transcribe_microphone("en-US", "google")
        
        self.assertIn("text", result)
        self.assertEqual(result["text"], "Hello world")
        self.assertEqual(result["engine"], "google")
    
    @patch('0099.sr.Microphone')
    @patch('0099.sr.Recognizer')
    def test_microphone_transcription_error(self, mock_recognizer_class, mock_microphone_class):
        """Test microphone transcription error handling."""
        # Mock the recognizer and microphone
        mock_recognizer = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        mock_recognizer.adjust_for_ambient_noise.return_value = None
        mock_recognizer.listen.side_effect = Exception("Microphone error")
        
        # Mock the microphone context manager
        mock_microphone = Mock()
        mock_microphone_class.return_value.__enter__.return_value = mock_microphone
        
        result = self.converter.transcribe_microphone("en-US", "google")
        
        self.assertIn("error", result)
        self.assertIn("Microphone error", result["error"])
    
    def test_unsupported_engine(self):
        """Test handling of unsupported recognition engine."""
        result = self.converter._process_audio(Mock(), "en-US", "unsupported_engine")
        
        self.assertIn("error", result)
        self.assertIn("Unsupported engine", result["error"])
    
    def test_google_recognition_success(self):
        """Test successful Google recognition."""
        # Mock audio object
        mock_audio = Mock()
        
        # Mock recognizer
        self.converter.recognizer.recognize_google.return_value = "Test transcription"
        
        result = self.converter._recognize_google(mock_audio, "en-US")
        
        self.assertEqual(result["text"], "Test transcription")
        self.assertEqual(result["engine"], "google")
        self.assertEqual(result["confidence"], 0.8)
    
    def test_google_recognition_unknown_value(self):
        """Test Google recognition with unknown value error."""
        # Mock audio object
        mock_audio = Mock()
        
        # Mock recognizer to raise UnknownValueError
        self.converter.recognizer.recognize_google.side_effect = Exception("Unknown value")
        
        result = self.converter._recognize_google(mock_audio, "en-US")
        
        self.assertIn("error", result)
        self.assertIn("Could not understand audio", result["error"])
    
    def test_whisper_recognition_success(self):
        """Test successful Whisper recognition."""
        # Mock audio object
        mock_audio = Mock()
        mock_audio.export.return_value = None
        
        # Mock whisper
        with patch('0099.whisper.load_model') as mock_load_model:
            mock_model = Mock()
            mock_model.transcribe.return_value = {"text": "Whisper transcription"}
            mock_load_model.return_value = mock_model
            
            with patch('tempfile.NamedTemporaryFile') as mock_temp_file:
                mock_temp_file.return_value.__enter__.return_value.name = "/tmp/test.wav"
                
                result = self.converter._recognize_whisper(mock_audio, "en-US")
                
                self.assertEqual(result["text"], "Whisper transcription")
                self.assertEqual(result["engine"], "whisper")
                self.assertEqual(result["confidence"], 0.9)
    
    def test_azure_recognition_no_credentials(self):
        """Test Azure recognition without credentials."""
        # Mock audio object
        mock_audio = Mock()
        
        result = self.converter._recognize_azure(mock_audio, "en-US")
        
        self.assertIn("error", result)
        self.assertIn("Azure credentials not configured", result["error"])
    
    def test_openai_recognition_no_credentials(self):
        """Test OpenAI recognition without credentials."""
        # Mock audio object
        mock_audio = Mock()
        
        result = self.converter._recognize_openai(mock_audio, "en-US")
        
        self.assertIn("error", result)
        self.assertIn("OpenAI API key not configured", result["error"])
    
    def test_save_transcription(self):
        """Test saving transcription to database."""
        test_result = {
            "text": "Test transcription",
            "confidence": 0.85,
            "metadata": {"test": "data"}
        }
        
        self.converter._save_transcription(test_result, "en-US", "google")
        
        # Check if transcription was saved
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT text, language, engine, confidence FROM transcriptions")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Test transcription")
        self.assertEqual(result[1], "en-US")
        self.assertEqual(result[2], "google")
        self.assertEqual(result[3], 0.85)
    
    def test_get_transcription_history(self):
        """Test retrieving transcription history."""
        # Add test data
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transcriptions (text, language, engine, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test 1", "en-US", "google", 0.8, "{}"))
        cursor.execute('''
            INSERT INTO transcriptions (text, language, engine, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test 2", "es-ES", "whisper", 0.9, "{}"))
        conn.commit()
        conn.close()
        
        history = self.converter.get_transcription_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["text"], "Test 2")  # Most recent first
        self.assertEqual(history[1]["text"], "Test 1")
    
    def test_export_transcriptions_json(self):
        """Test exporting transcriptions as JSON."""
        # Add test data
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transcriptions (text, language, engine, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test transcription", "en-US", "google", 0.8, "{}"))
        conn.commit()
        conn.close()
        
        export_data = self.converter.export_transcriptions("json")
        
        self.assertIsInstance(export_data, str)
        parsed_data = json.loads(export_data)
        self.assertEqual(len(parsed_data), 1)
        self.assertEqual(parsed_data[0]["text"], "Test transcription")
    
    def test_export_transcriptions_csv(self):
        """Test exporting transcriptions as CSV."""
        # Add test data
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transcriptions (text, language, engine, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test transcription", "en-US", "google", 0.8, "{}"))
        conn.commit()
        conn.close()
        
        export_data = self.converter.export_transcriptions("csv")
        
        self.assertIsInstance(export_data, str)
        self.assertIn("Test transcription", export_data)
        self.assertIn("en-US", export_data)
    
    def test_export_transcriptions_txt(self):
        """Test exporting transcriptions as TXT."""
        # Add test data
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transcriptions (text, language, engine, confidence, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test transcription", "en-US", "google", 0.8, "{}"))
        conn.commit()
        conn.close()
        
        export_data = self.converter.export_transcriptions("txt")
        
        self.assertIsInstance(export_data, str)
        self.assertIn("Test transcription", export_data)
    
    def test_export_transcriptions_unsupported_format(self):
        """Test exporting transcriptions with unsupported format."""
        with self.assertRaises(ValueError):
            self.converter.export_transcriptions("unsupported")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        test_config = {
            "google_api_key": "",
            "azure_key": "",
            "azure_region": "",
            "openai_api_key": "",
            "whisper_model": "base",
            "default_language": "en-US",
            "supported_languages": {
                "en-US": "English (US)"
            },
            "audio_settings": {
                "sample_rate": 16000,
                "channels": 1,
                "format": "wav"
            }
        }
        json.dump(test_config, self.temp_config)
        self.temp_config.close()
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        try:
            os.unlink(self.temp_db.name)
            os.unlink(self.temp_config.name)
        except OSError:
            pass
    
    @patch('0099.sqlite3.connect')
    def test_full_workflow(self, mock_connect):
        """Test complete workflow from transcription to export."""
        mock_connect.return_value = sqlite3.connect(self.temp_db.name)
        converter = SpeechToTextConverter(self.temp_config.name)
        
        # Mock successful transcription
        with patch.object(converter, 'transcribe_microphone') as mock_transcribe:
            mock_transcribe.return_value = {
                "text": "Integration test transcription",
                "confidence": 0.9,
                "engine": "google"
            }
            
            # Perform transcription
            result = converter.transcribe_microphone("en-US", "google")
            
            # Verify result
            self.assertEqual(result["text"], "Integration test transcription")
            
            # Get history
            history = converter.get_transcription_history()
            self.assertEqual(len(history), 1)
            
            # Export data
            export_data = converter.export_transcriptions("json")
            parsed_data = json.loads(export_data)
            self.assertEqual(len(parsed_data), 1)
            self.assertEqual(parsed_data[0]["text"], "Integration test transcription")


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSpeechToTextConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)

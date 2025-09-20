# Speech-to-Text Converter

A modern, feature-rich speech-to-text converter with multiple recognition engines, web interface, database storage, and advanced analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

### Core Functionality
- **Multiple Recognition Engines**: Google Speech API, OpenAI Whisper, Azure Speech Services, OpenAI API
- **Real-time Transcription**: Live microphone input with instant processing
- **File Upload Support**: Process audio files in various formats (WAV, MP3, M4A, FLAC, OGG)
- **Multi-language Support**: 40+ languages including English, Spanish, French, German, Japanese, Chinese, and more
- **Database Storage**: SQLite database for transcription history and analytics

### User Interface
- **Modern Web UI**: Beautiful Streamlit interface with responsive design
- **Interactive Dashboard**: Real-time analytics and visualization
- **Search & Filter**: Advanced search and filtering capabilities
- **Export Options**: Multiple export formats (JSON, CSV, TXT)

### Analytics & Insights
- **Usage Statistics**: Track transcription counts, confidence scores, and language usage
- **Visual Analytics**: Charts and graphs for data visualization
- **Performance Metrics**: Engine comparison and accuracy tracking
- **Historical Data**: Complete transcription history with timestamps

### Advanced Features
- **Configurable Settings**: Customizable recognition parameters
- **API Integration**: Support for multiple cloud speech services
- **Audio Processing**: Automatic format conversion and optimization
- **Error Handling**: Robust error handling and user feedback
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone access
- Internet connection (for cloud APIs)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/speech-to-text-converter.git
   cd speech-to-text-converter
   ```

2. **Install system dependencies**

   **macOS:**
   ```bash
   brew install portaudio
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio
   ```

   **Windows:**
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys (optional)**
   
   Edit `config.json` and add your API keys:
   ```json
   {
     "google_api_key": "your_google_api_key",
     "azure_key": "your_azure_key",
     "azure_region": "your_azure_region",
     "openai_api_key": "your_openai_api_key"
   }
   ```

### Running the Application

1. **Web Interface (Recommended)**
   ```bash
   streamlit run app.py
   ```
   Open your browser to `http://localhost:8501`

2. **Command Line Interface**
   ```bash
   python 0099.py
   ```

## Usage Guide

### Web Interface

1. **Live Transcription**
   - Select your preferred language and recognition engine
   - Click "Start Recording" and speak clearly
   - View your transcription instantly

2. **File Upload**
   - Upload audio files in supported formats
   - Choose language and engine settings
   - Process and view transcriptions

3. **History Management**
   - Browse all previous transcriptions
   - Search and filter by language, engine, or keywords
   - Export data in multiple formats

4. **Analytics Dashboard**
   - View usage statistics and trends
   - Analyze language distribution
   - Compare engine performance

### Command Line Interface

The CLI provides a menu-driven interface with options for:
- Microphone transcription
- File transcription
- History viewing
- Data export

## 🔧 Configuration

### Recognition Engines

| Engine | Description | API Key Required | Offline Support |
|--------|-------------|------------------|-----------------|
| Google | Google Speech API | No | No |
| Whisper | OpenAI Whisper | No | Yes |
| Azure | Azure Speech Services | Yes | No |
| OpenAI | OpenAI API | Yes | No |

### Supported Languages

The application supports 40+ languages including:
- **European**: English, Spanish, French, German, Italian, Portuguese, Russian, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Turkish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Slovak, Slovenian, Estonian, Latvian, Lithuanian, Maltese, Welsh, Irish, Icelandic, Macedonian, Albanian, Serbian, Bosnian, Montenegrin
- **Asian**: Japanese, Korean, Chinese (Simplified), Thai, Vietnamese, Hindi
- **Middle Eastern**: Arabic, Hebrew
- **Others**: Ukrainian

### Audio Settings

Configure audio processing parameters in `config.json`:
```json
{
  "audio_settings": {
    "sample_rate": 16000,
    "channels": 1,
    "format": "wav",
    "chunk_size": 1024,
    "timeout": 10,
    "phrase_time_limit": 30
  }
}
```

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE transcriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    language TEXT,
    engine TEXT,
    audio_file_path TEXT,
    confidence REAL,
    duration REAL,
    metadata TEXT
);
```

## API Reference

### SpeechToTextConverter Class

#### Methods

- `transcribe_microphone(language, engine)` - Transcribe from microphone
- `transcribe_file(file_path, language, engine)` - Transcribe from file
- `get_transcription_history(limit)` - Get transcription history
- `export_transcriptions(format)` - Export transcriptions

#### Parameters

- `language`: Language code (e.g., "en-US", "es-ES")
- `engine`: Recognition engine ("google", "whisper", "azure", "openai")
- `format`: Export format ("json", "csv", "txt")

## Testing

Run the test suite:
```bash
pytest tests/
```

Run specific tests:
```bash
pytest tests/test_converter.py
pytest tests/test_ui.py
```

## 📁 Project Structure

```
speech-to-text-converter/
├── 0099.py                 # Core converter class
├── app.py                  # Streamlit web interface
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── tests/                # Test files
│   ├── test_converter.py
│   └── test_ui.py
├── transcriptions.db     # SQLite database (created automatically)
└── examples/             # Example audio files
    └── sample.wav
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy
   ```

2. Run code formatting:
   ```bash
   black .
   ```

3. Run linting:
   ```bash
   flake8 .
   ```

4. Run type checking:
   ```bash
   mypy .
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Python speech recognition library
- [Streamlit](https://streamlit.io/) - Web application framework
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition model
- [Google Speech API](https://cloud.google.com/speech-to-text) - Cloud speech recognition
- [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/) - Microsoft speech services

## Roadmap

### Upcoming Features
- [ ] Real-time streaming transcription
- [ ] Custom vocabulary support
- [ ] Speaker identification
- [ ] Emotion detection
- [ ] Multi-speaker diarization
- [ ] Cloud deployment options
- [ ] Mobile app version
- [ ] Plugin system for custom engines

### Version History

- **v1.0.0** - Initial release with basic functionality
- **v1.1.0** - Added web interface and database storage
- **v1.2.0** - Added multiple recognition engines
- **v1.3.0** - Added analytics dashboard and export features
- **v1.4.0** - Added 40+ language support and advanced configuration


# Speech-to-Text-Converter

#!/usr/bin/env python3
"""
Example Audio File Generator
===========================

This script generates example audio files for testing the
speech-to-text converter.
"""

import numpy as np
import wave
import os
from pathlib import Path


def generate_sine_wave(frequency, duration, sample_rate=16000):
    """Generate a sine wave audio signal."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    return (wave_data * 32767).astype(np.int16)


def create_example_audio_files():
    """Create example audio files for testing."""
    # Create examples directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Generate different types of audio files
    sample_rate = 16000
    
    # 1. Simple sine wave (440 Hz for 2 seconds)
    print("🎵 Generating sine wave example...")
    sine_wave = generate_sine_wave(440, 2, sample_rate)
    
    with wave.open("examples/sine_wave.wav", "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(sine_wave.tobytes())
    
    # 2. Multiple frequency sweep
    print("🎵 Generating frequency sweep...")
    duration = 3
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequencies = np.linspace(200, 800, len(t))
    sweep_wave = np.sin(2 * np.pi * frequencies * t)
    sweep_wave = (sweep_wave * 32767).astype(np.int16)
    
    with wave.open("examples/frequency_sweep.wav", "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(sweep_wave.tobytes())
    
    # 3. White noise
    print("🎵 Generating white noise...")
    noise_duration = 1
    noise_samples = int(sample_rate * noise_duration)
    white_noise = np.random.normal(0, 0.1, noise_samples)
    white_noise = (white_noise * 32767).astype(np.int16)
    
    with wave.open("examples/white_noise.wav", "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(white_noise.tobytes())
    
    # 4. Silence
    print("🎵 Generating silence...")
    silence_duration = 2
    silence_samples = int(sample_rate * silence_duration)
    silence = np.zeros(silence_samples, dtype=np.int16)
    
    with wave.open("examples/silence.wav", "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(silence.tobytes())
    
    print("✅ Example audio files created successfully!")
    print("\n📁 Generated files:")
    for file_path in examples_dir.glob("*.wav"):
        file_size = file_path.stat().st_size
        print(f"  - {file_path.name} ({file_size} bytes)")


def create_test_script():
    """Create a test script for the audio files."""
    test_script = '''#!/usr/bin/env python3
"""
Test script for example audio files
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 0099 import SpeechToTextConverter

def test_audio_files():
    """Test transcription of example audio files."""
    converter = SpeechToTextConverter()
    examples_dir = Path("examples")
    
    if not examples_dir.exists():
        print("❌ Examples directory not found. Run create_examples.py first.")
        return
    
    print("🧪 Testing example audio files...")
    
    for audio_file in examples_dir.glob("*.wav"):
        print(f"\\n🎵 Testing {audio_file.name}...")
        
        try:
            result = converter.transcribe_file(str(audio_file), "en-US", "google")
            
            if "error" in result:
                print(f"  ❌ Error: {result['error']}")
            else:
                print(f"  ✅ Transcription: {result['text']}")
                print(f"  📊 Confidence: {result.get('confidence', 'N/A')}")
        
        except Exception as e:
            print(f"  ❌ Exception: {e}")

if __name__ == "__main__":
    test_audio_files()
'''
    
    with open("test_examples.py", "w") as f:
        f.write(test_script)
    
    print("📄 Created test script: test_examples.py")


def main():
    """Main function."""
    print("🎵 Example Audio File Generator")
    print("=" * 40)
    
    try:
        create_example_audio_files()
        create_test_script()
        
        print("\n🎉 Setup completed!")
        print("\n📖 Usage:")
        print("1. Run the test script: python test_examples.py")
        print("2. Use the files in the web interface or CLI")
        print("3. Files are located in the 'examples' directory")
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install numpy with: pip install numpy")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Setup script for Advanced Speech-to-Text Converter
==================================================

This script helps set up the environment and install dependencies
for the speech-to-text converter.
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_system_dependencies():
    """Install system dependencies based on the operating system."""
    system = platform.system().lower()
    
    print(f"🖥️  Detected OS: {system}")
    
    if system == "darwin":  # macOS
        print("📦 Installing system dependencies for macOS...")
        try:
            subprocess.run(["brew", "install", "portaudio"], check=True)
            print("✅ PortAudio installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PortAudio. Please install Homebrew first.")
            return False
        except FileNotFoundError:
            print("❌ Homebrew not found. Please install Homebrew first.")
            return False
    
    elif system == "linux":
        print("📦 Installing system dependencies for Linux...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "portaudio19-dev", "python3-pyaudio"], check=True)
            print("✅ PortAudio installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PortAudio. Please run manually:")
            print("sudo apt-get update")
            print("sudo apt-get install -y portaudio19-dev python3-pyaudio")
            return False
    
    elif system == "windows":
        print("📦 Installing system dependencies for Windows...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pipwin"], check=True)
            subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio"], check=True)
            print("✅ PyAudio installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyAudio. Please install manually.")
            return False
    
    return True


def install_python_dependencies():
    """Install Python dependencies from requirements.txt."""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False


def create_directories():
    """Create necessary directories."""
    directories = ["tests", "examples", "logs", "exports"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")


def create_example_files():
    """Create example files."""
    # Create example config
    example_config = {
        "google_api_key": "your_google_api_key_here",
        "azure_key": "your_azure_key_here",
        "azure_region": "your_azure_region_here",
        "openai_api_key": "your_openai_api_key_here",
        "whisper_model": "base",
        "default_language": "en-US",
        "supported_languages": {
            "en-US": "English (US)",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German"
        },
        "audio_settings": {
            "sample_rate": 16000,
            "channels": 1,
            "format": "wav"
        }
    }
    
    with open("config.example.json", "w") as f:
        json.dump(example_config, f, indent=2)
    
    print("📄 Created example config: config.example.json")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
config.json
transcriptions.db
*.wav
*.mp3
*.m4a
*.flac
*.ogg
exports/
logs/
temp/

# API keys
.env
secrets.json
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("📄 Created .gitignore")


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        return False
    except FileNotFoundError:
        print("⚠️  pytest not found. Install with: pip install pytest")
        return False


def main():
    """Main setup function."""
    print("🎤 Advanced Speech-to-Text Converter Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies():
        print("⚠️  System dependencies installation failed. Continuing anyway...")
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Python dependencies installation failed!")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create example files
    create_example_files()
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed. Please check the installation.")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Copy config.example.json to config.json and add your API keys")
    print("2. Run the web interface: streamlit run app.py")
    print("3. Or run the CLI: python 0099.py")
    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()

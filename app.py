"""
Streamlit Web Interface for Advanced Speech-to-Text Converter
============================================================

A modern web interface for the speech-to-text converter with real-time
transcription, file upload, history management, and export features.
"""

import streamlit as st
import pandas as pd
import json
import tempfile
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import importlib.util
import sys

# Import the main converter module
spec = importlib.util.spec_from_file_location("converter", "0099.py")
converter_module = importlib.util.module_from_spec(spec)
sys.modules["converter"] = converter_module
spec.loader.exec_module(converter_module)

SpeechToTextConverter = converter_module.SpeechToTextConverter

# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Speech-to-Text Converter",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    
    .transcription-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the converter
@st.cache_resource
def get_converter():
    """Get cached converter instance."""
    return SpeechToTextConverter()

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🎤 Advanced Speech-to-Text Converter</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Language selection
        languages = {
            "en-US": "English (US)",
            "en-GB": "English (UK)",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German",
            "it-IT": "Italian",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese (Simplified)"
        }
        
        selected_language = st.selectbox(
            "🌍 Select Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=0
        )
        
        # Engine selection
        engines = {
            "google": "Google Speech API",
            "whisper": "OpenAI Whisper",
            "azure": "Azure Speech Services",
            "openai": "OpenAI API"
        }
        
        selected_engine = st.selectbox(
            "🔧 Select Engine",
            options=list(engines.keys()),
            format_func=lambda x: engines[x],
            index=0
        )
        
        st.divider()
        
        # Statistics
        st.header("📊 Statistics")
        converter = get_converter()
        history = converter.get_transcription_history(1000)
        
        if history:
            total_transcriptions = len(history)
            avg_confidence = sum(item.get('confidence', 0) for item in history) / total_transcriptions
            languages_used = len(set(item.get('language', '') for item in history))
            
            st.metric("Total Transcriptions", total_transcriptions)
            st.metric("Average Confidence", f"{avg_confidence:.2f}")
            st.metric("Languages Used", languages_used)
        else:
            st.info("No transcriptions yet!")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎤 Live Transcription", 
        "📁 File Upload", 
        "📚 History", 
        "📊 Analytics", 
        "⚙️ Settings"
    ])
    
    with tab1:
        st.header("🎤 Live Microphone Transcription")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🎤 Start Recording", type="primary", use_container_width=True):
                with st.spinner("Listening... Please speak now!"):
                    result = converter.transcribe_microphone(selected_language, selected_engine)
                
                if "error" in result:
                    st.markdown(f'<div class="error-message">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-message">✅ Transcription completed!</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="transcription-box"><strong>📝 Transcription:</strong><br>{result["text"]}</div>', unsafe_allow_html=True)
                    
                    # Show additional info
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("Confidence", f"{result.get('confidence', 0):.2f}")
                    with col_info2:
                        st.metric("Engine", result.get('engine', 'Unknown'))
                    with col_info3:
                        st.metric("Language", selected_language)
        
        with col2:
            st.info("""
            **Instructions:**
            1. Click "Start Recording"
            2. Speak clearly into your microphone
            3. Wait for processing
            4. View your transcription
            
            **Tips:**
            - Speak clearly and at normal pace
            - Reduce background noise
            - Use a good quality microphone
            """)
    
    with tab2:
        st.header("📁 Upload Audio File")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
            help="Supported formats: WAV, MP3, M4A, FLAC, OGG"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🔄 Transcribe File", type="primary", use_container_width=True):
                    with st.spinner("Processing audio file..."):
                        result = converter.transcribe_file(tmp_path, selected_language, selected_engine)
                    
                    if "error" in result:
                        st.markdown(f'<div class="error-message">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="success-message">✅ File transcribed successfully!</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="transcription-box"><strong>📝 Transcription:</strong><br>{result["text"]}</div>', unsafe_allow_html=True)
                        
                        # Show file info
                        st.info(f"📁 File: {uploaded_file.name}")
            
            with col2:
                st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
            
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    with tab3:
        st.header("📚 Transcription History")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_text = st.text_input("🔍 Search transcriptions", placeholder="Enter keywords...")
        
        with col2:
            filter_language = st.selectbox(
                "🌍 Filter by Language",
                options=["All"] + list(languages.keys()),
                format_func=lambda x: languages.get(x, x)
            )
        
        with col3:
            filter_engine = st.selectbox(
                "🔧 Filter by Engine",
                options=["All"] + list(engines.keys()),
                format_func=lambda x: engines.get(x, x)
            )
        
        # Filter history
        filtered_history = history.copy()
        
        if search_text:
            filtered_history = [item for item in filtered_history if search_text.lower() in item.get('text', '').lower()]
        
        if filter_language != "All":
            filtered_history = [item for item in filtered_history if item.get('language') == filter_language]
        
        if filter_engine != "All":
            filtered_history = [item for item in filtered_history if item.get('engine') == filter_engine]
        
        # Display history
        if filtered_history:
            st.write(f"Found {len(filtered_history)} transcriptions")
            
            for i, item in enumerate(filtered_history[:20]):  # Show first 20
                with st.expander(f"📝 {item['timestamp']} - {item['text'][:50]}..."):
                    st.write(f"**Text:** {item['text']}")
                    st.write(f"**Language:** {item.get('language', 'Unknown')}")
                    st.write(f"**Engine:** {item.get('engine', 'Unknown')}")
                    st.write(f"**Confidence:** {item.get('confidence', 0):.2f}")
                    st.write(f"**Timestamp:** {item['timestamp']}")
        else:
            st.info("No transcriptions found matching your criteria.")
        
        # Export options
        st.subheader("📤 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as JSON", use_container_width=True):
                export_data = converter.export_transcriptions("json")
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as CSV", use_container_width=True):
                export_data = converter.export_transcriptions("csv")
                st.download_button(
                    label="Download CSV",
                    data=export_data,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📝 Export as TXT", use_container_width=True):
                export_data = converter.export_transcriptions("txt")
                st.download_button(
                    label="Download TXT",
                    data=export_data,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    with tab4:
        st.header("📊 Analytics Dashboard")
        
        if history:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Transcriptions over time
                daily_counts = df.groupby('date').size().reset_index(name='count')
                fig_time = px.line(daily_counts, x='date', y='count', title='Transcriptions Over Time')
                st.plotly_chart(fig_time, use_container_width=True)
            
            with col2:
                # Language distribution
                lang_counts = df['language'].value_counts()
                fig_lang = px.pie(values=lang_counts.values, names=lang_counts.index, title='Language Distribution')
                st.plotly_chart(fig_lang, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Engine usage
                engine_counts = df['engine'].value_counts()
                fig_engine = px.bar(x=engine_counts.index, y=engine_counts.values, title='Engine Usage')
                st.plotly_chart(fig_engine, use_container_width=True)
            
            with col4:
                # Confidence distribution
                if 'confidence' in df.columns:
                    fig_conf = px.histogram(df, x='confidence', title='Confidence Distribution', nbins=20)
                    st.plotly_chart(fig_conf, use_container_width=True)
            
            # Summary statistics
            st.subheader("📈 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Transcriptions", len(df))
            
            with col2:
                st.metric("Unique Languages", df['language'].nunique())
            
            with col3:
                st.metric("Average Confidence", f"{df['confidence'].mean():.2f}")
            
            with col4:
                st.metric("Most Used Engine", df['engine'].mode().iloc[0] if not df.empty else "N/A")
        
        else:
            st.info("No data available for analytics. Start transcribing to see insights!")
    
    with tab5:
        st.header("⚙️ Settings & Configuration")
        
        # API Keys configuration
        st.subheader("🔑 API Configuration")
        
        with st.form("api_config"):
            google_key = st.text_input("Google API Key (optional)", type="password")
            azure_key = st.text_input("Azure Speech Key (optional)", type="password")
            azure_region = st.text_input("Azure Region (optional)")
            openai_key = st.text_input("OpenAI API Key (optional)", type="password")
            
            if st.form_submit_button("💾 Save Configuration"):
                # Save configuration (in a real app, you'd want to encrypt these)
                config = {
                    "google_api_key": google_key,
                    "azure_key": azure_key,
                    "azure_region": azure_region,
                    "openai_api_key": openai_key,
                    "whisper_model": "base",
                    "default_language": selected_language,
                    "supported_languages": languages,
                    "audio_settings": {
                        "sample_rate": 16000,
                        "channels": 1,
                        "format": "wav"
                    }
                }
                
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=2)
                
                st.success("Configuration saved successfully!")
        
        # Database management
        st.subheader("🗄️ Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All History", type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    # Clear database
                    import sqlite3
                    conn = sqlite3.connect("transcriptions.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM transcriptions")
                    conn.commit()
                    conn.close()
                    st.success("All transcription history cleared!")
                    st.session_state.confirm_clear = False
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm clearing all history")
        
        with col2:
            if st.button("📊 Database Stats"):
                import sqlite3
                conn = sqlite3.connect("transcriptions.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM transcriptions")
                count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(DISTINCT language) FROM transcriptions")
                lang_count = cursor.fetchone()[0]
                conn.close()
                
                st.info(f"Total records: {count}\nUnique languages: {lang_count}")
        
        # About section
        st.subheader("ℹ️ About")
        st.info("""
        **Advanced Speech-to-Text Converter**
        
        This application provides:
        - Multiple speech recognition engines
        - Real-time microphone transcription
        - Audio file upload and processing
        - Transcription history with database storage
        - Multiple language support
        - Export options (JSON, CSV, TXT)
        - Analytics dashboard
        
        Built with Python, Streamlit, and modern speech recognition libraries.
        """)

if __name__ == "__main__":
    main()

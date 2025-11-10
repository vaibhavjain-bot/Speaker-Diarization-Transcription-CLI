# 🎧 WhisperDiarize

**Speaker Diarization + Transcription CLI using PyAnnote 3.1 & OpenAI Whisper**

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-pyannote--3.1-orange)
![GPU](https://img.shields.io/badge/GPU-supported-brightgreen)

---

## 🚀 Features

- **Speaker Diarization**: Automatically identifies different speakers in audio  
- **Speech Transcription**: Converts speech to text using Whisper  
- **Speaker-Attributed Transcripts**: Each line shows who spoke, when, and what they said  
- **Automatic Dependency Management**: Checks and installs missing packages  
- **Progress Monitoring**: Real-time updates during processing  
- **CPU/GPU Support**: Works without GPU; uses GPU automatically if available  
- **Timestamped Output**: Timestamps in `mm:ss` format  

---

## 🧩 Requirements

- Python 3.10+  
- Hugging Face account and token (free)  

### Dependencies

The script automatically checks for and can install:

- `torch`  
- `torchaudio`  
- `soundfile`  
- `pyannote-audio=4.0.1`  
- `openai-whisper`  

---

## ⚙️ Installation

1. Clone or download the repository  
2. Make the script executable (Linux/Mac):
```bash
chmod +x diarize_transcribe.py


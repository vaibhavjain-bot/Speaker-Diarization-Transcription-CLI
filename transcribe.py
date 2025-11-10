# Speaker Diarization + Transcription CLI

A Python command-line tool that performs speaker diarization (identifying who spoke when) and transcription on audio files. The tool uses PyAnnote for diarization and OpenAI's Whisper for transcription.

## Features

- **Speaker Diarization**: Automatically identifies different speakers in audio
- **Speech Transcription**: Converts speech to text using Whisper
- **Speaker-Attributed Transcripts**: Each line shows who spoke, when, and what they said
- **Automatic Dependency Management**: Checks and installs missing packages
- **Progress Monitoring**: Real-time progress updates during processing
- **CPU-Only Support**: Works without GPU (though GPU is used if available)
- **Timestamped Output**: Shows timestamps in `mm:ss` format

## Requirements

- Python 3.7+
- Hugging Face account and token (free)

### Dependencies

The script automatically checks for and can install:
- `torch`
- `torchaudio`
- `soundfile`
- `pyannote-audio`
- `openai-whisper`

## Installation

1. Clone or download the script
2. Make it executable (Linux/Mac):
   ```bash
   chmod +x diarize_transcribe.py
   ```

3. Check and install dependencies:
   ```bash
   python diarize_transcribe.py --check-deps
   ```

## Setup

### Get a Hugging Face Token

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Go to Settings → Access Tokens
3. Create a new token with read permissions
4. Accept the PyAnnote model terms at [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1)

### Configure Token

You can provide your token in three ways:

**Option 1: Environment variable (recommended)**
```bash
export HF_TOKEN="your_token_here"
```

**Option 2: Command-line argument**
```bash
python diarize_transcribe.py audio.wav --hf-token your_token_here
```

**Option 3: Edit the script**
Replace `YOUR_HF_TOKEN_HERE` in the script with your actual token.

## Usage

### Basic Usage

```bash
python diarize_transcribe.py audio.wav
```

### With Options

```bash
# Use a larger Whisper model for better accuracy
python diarize_transcribe.py audio.wav --whisper-model medium

# Provide HF token explicitly
python diarize_transcribe.py audio.wav --hf-token your_token_here
```

### Whisper Model Options

Choose a model based on accuracy vs. speed tradeoff:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 39 MB | Fastest | Lowest |
| `base` | 74 MB | Fast | Low |
| `small` | 244 MB | Medium | Medium |
| `medium` | 769 MB | Slow | High |
| `large` | 1550 MB | Slowest | Highest |

Default is `tiny` for quick processing.

## Output

The script creates a text file named `{original_filename}_diarization.txt` in the same directory as your input file.

### Output Format

```
[SPEAKER_00] [00:05-00:12]: Hello everyone, welcome to today's meeting.
[SPEAKER_01] [00:13-00:20]: Thanks for having me. I'd like to discuss the project timeline.
[SPEAKER_00] [00:21-00:28]: Sure, let's start with the current status.
```

Each line contains:
- Speaker label (e.g., `SPEAKER_00`, `SPEAKER_01`)
- Start and end timestamps in `mm:ss` format
- Transcribed text

## Example

```bash
# Process a meeting recording
python diarize_transcribe.py meeting.wav --whisper-model small

# Output:
# Checking dependencies...
# ✓ torch is installed
# ✓ torchaudio is installed
# ...
# Loading audio: meeting.wav
# Running speaker diarization...
# Diarization completed.
# Loading Whisper model (small)...
# [SPEAKER_00] [00:05-00:12]: Hello everyone...
# ...
# Transcription saved to: meeting_diarization.txt
```

## Supported Audio Formats

- WAV (recommended)
- MP3
- Any format supported by `soundfile`

## Performance Notes

- **First run**: Downloads models (may take several minutes)
- **GPU**: Automatically used if available, significantly faster
- **CPU**: Works fine but slower, especially with larger Whisper models
- **Memory**: Audio is loaded entirely into RAM for processing

## Troubleshooting

### "Missing packages" error
Run with `--check-deps` flag to install dependencies:
```bash
python diarize_transcribe.py --check-deps
```

### "Hugging Face token is required" error
Set your token via environment variable or command-line argument (see Setup section).

### "You must agree to the terms" error
Visit the [PyAnnote model page](https://huggingface.co/pyannote/speaker-diarization-community-1) and accept the terms while logged in.

### Slow processing
- Use a smaller Whisper model (`--whisper-model tiny`)
- Ensure you have a GPU available
- Close other applications to free up resources

## Credits

- [PyAnnote Audio](https://github.com/pyannote/pyannote-audio) for speaker diarization
- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition

## License

This script is provided as-is for personal and educational use. Please respect the licenses of the underlying libraries (PyAnnote and Whisper).
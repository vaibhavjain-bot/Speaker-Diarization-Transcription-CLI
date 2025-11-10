# Speaker Diarization + Transcription CLI

A Python CLI tool for speaker diarization and transcription using `pyannote.audio` and `whisper`. Preloads audio into memory, supports progress monitoring, and outputs timestamps in `mm:ss` format.

---

## Features
- Speaker Diarization: Identify who speaks when in an audio file.
- Transcription: Convert speech to text with timestamps.
- Dependency Check: Automatically checks and installs required packages.
- Progress Monitoring: Real-time progress updates during processing.
- CPU/GPU Support: Runs on CPU by default, uses GPU if available.
- Timestamp Formatting: Outputs timestamps in `mm:ss` for readability.

---

## Requirements
- **Python**: 3.10 or above
- **Dependencies**:
  - `torch`
  - `torchaudio`
  - `soundfile`
  - `pyannote.audio` (version 4.0.1)
  - `openai-whisper`

---

## Installation

### 1. Clone the Repository
```bash
gh repo clone vaibhavjain-bot/Speaker-Diarization-Transcription-CLI
```

### 2. Install Dependencies
Run the script with the `--check-deps` flag to automatically check and install missing packages:
```bash
python diarization_transcription.py --check-deps
```
Or manually install dependencies:
```bash
pip install torch torchaudio soundfile pyannote-audio==4.0.1 openai-whisper
```

---

## Usage

### 1. Set Up Hugging Face Token
- Sign up at [Hugging Face](https://huggingface.co/) and get your API token.
- Export the token as an environment variable:
  ```bash
  export HF_TOKEN="your_huggingface_token_here"
  ```
  Or pass it directly via the CLI:
  ```bash
  python diarization_transcription.py --hf-token "your_huggingface_token_here" audio_file.wav
  ```

### 2. Run the Tool
```bash
python diarization_transcription.py audio_file.wav --whisper-model tiny
```
Replace `audio_file.wav` with your audio file path and `tiny` with your preferred Whisper model size (`tiny`, `base`, `small`, `medium`, `large`).

---

## Example Output
The tool generates a text file with the following format:
```
[SPEAKER_01] [00:00-00:05]: Hello, how are you?
[SPEAKER_02] [00:05-00:10]: I'm good, thanks!
```

---

## Arguments
| Argument          | Description                                      | Required |
|-------------------|--------------------------------------------------|----------|
| `file`            | Path to the WAV/MP3 audio file                   | Yes      |
| `--hf-token`      | Hugging Face token                                | No*      |
| `--whisper-model` | Whisper model size (`tiny`, `base`, `small`, etc.)| No       |
| `--check-deps`    | Check and install required packages              | No       |

\* Required if not set as an environment variable.

---

## Notes
- Hugging Face Token: Required for `pyannote.audio` to work.
- GPU Support: Automatically detected and used if available.
- Output: Results are saved as `[input_filename]_diarization.txt`.

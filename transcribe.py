#!/usr/bin/env python3
"""
Speaker diarization + transcription CLI
- Preloads audio into memory
- CPU-only
- Progress monitoring
- Automatic dependency check
- Timestamps in minutes:seconds
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# -----------------------------
# Dependency Check
# -----------------------------
REQUIRED_PACKAGES = {
    "torch": "torch",
    "torchaudio": "torchaudio",
    "soundfile": "soundfile",
    "pyannote.audio": "pyannote-audio",
    "whisper": "openai-whisper"
}

def check_and_install_packages():
    """Check for required packages and install missing ones"""
    missing = []
    print("Checking dependencies...\n")
    for module, package in REQUIRED_PACKAGES.items():
        try:
            __import__(module.split(".")[0])
            print(f"✓ {module} is installed")
        except ImportError:
            print(f"✗ {module} is missing")
            missing.append(package)

    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        response = input("Install missing packages now? (y/n): ").lower()
        if response != "y":
            print("Cannot proceed without required packages.")
            sys.exit(1)
        for package in missing:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("\nDependencies installed successfully!\n")
    else:
        print("\nAll dependencies are satisfied!\n")


# -----------------------------
# Helper: Format time as mm:ss
# -----------------------------
def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


# -----------------------------
# Diarization + Transcription
# -----------------------------
import torch
import soundfile as sf
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import whisper

def diarize_and_transcribe(file_path, hf_token, model_size="tiny"):
    # Load pipeline
    print("Loading diarization pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1",
        token=hf_token
    )

    # Load audio into memory
    print(f"Loading audio: {file_path}")
    waveform, sample_rate = sf.read(file_path)
    waveform = torch.from_numpy(waveform).float()
    if waveform.ndim > 1:
        waveform = waveform.mean(axis=1)
    waveform = waveform.unsqueeze(0)
    audio_dict = {"waveform": waveform, "sample_rate": sample_rate}

    # Run pipeline with progress hook
    print("Running speaker diarization...")
    with ProgressHook() as hook:
        diarization = pipeline(audio_dict, hook=hook)

    print("\nDiarization completed.")

    # Load Whisper model
    print(f"Loading Whisper model ({model_size})...")
    whisper_model = whisper.load_model(model_size)

    # Prepare output file
    input_path = Path(file_path)
    output_file = input_path.with_name(f"{input_path.stem}_diarization.txt")

    # Transcribe segments
    with open(output_file, "w", encoding="utf-8") as f:
        for turn, speaker in diarization.speaker_diarization:
            start = turn.start
            end = turn.end

            # Format timestamps in mm:ss
            start_fmt = format_time(start)
            end_fmt = format_time(end)

            # Extract segment waveform
            start_sample = int(start * sample_rate)
            end_sample = int(end * sample_rate)
            segment_waveform = waveform[0, start_sample:end_sample].numpy()

            # Save temporary WAV segment for Whisper
            segment_path = input_path.with_name("segment_temp.wav")
            sf.write(segment_path, segment_waveform, sample_rate)

            # Transcribe segment
            result = whisper_model.transcribe(str(segment_path))
            transcript = result["text"].strip()

            # Write to file and print
            line = f"[{speaker}] [{start_fmt}-{end_fmt}]: {transcript}"
            f.write(line + "\n")
            print(line)

    print(f"\nTranscription saved to: {output_file}")


# -----------------------------
# CLI Entry Point
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Speaker diarization + transcription CLI")
    parser.add_argument("file", help="Path to WAV/MP3 file")
    parser.add_argument("--hf-token", help="Hugging Face token", required=False)
    parser.add_argument("--whisper-model", default="tiny", help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--check-deps", action="store_true", help="Check and install required packages")
    args = parser.parse_args()

    if args.check_deps:
        check_and_install_packages()
        return

    hf_token = args.hf_token or os.environ.get("HF_TOKEN") or "YOUR_HF_TOKEN_HERE"
    if not hf_token:
        print("Error: Hugging Face token is required. Provide via --hf-token or HF_TOKEN environment variable.")
        sys.exit(1)

    diarize_and_transcribe(args.file, hf_token, model_size=args.whisper_model)


if __name__ == "__main__":
    main()

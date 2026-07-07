"""
services/preprocess.py
────────────────────────────────────────────────────────────
Cleans raw transcript text and chunks it for embedding.
"""

import re
import os
import json
from typing import List, Dict
from config import Config


# Filler words / patterns to clean
_FILLERS = re.compile(
    r"\b(um|uh|hmm|you know|like|basically|actually|so|right|okay|ok|"
    r"alright|now|let me|let's see|you see|i mean|kind of|sort of|"
    r"you know what i mean)\b",
    re.IGNORECASE,
)

_MULTI_SPACE = re.compile(r"\s{2,}")
_MUSIC_TAG   = re.compile(r"\[.*?\]|\(.*?\)")  # [Music], (applause), etc.


def clean_text(text: str) -> str:
    """Remove noise from transcript text."""
    text = _MUSIC_TAG.sub(" ", text)
    text = _FILLERS.sub(" ", text)
    text = _MULTI_SPACE.sub(" ", text)
    return text.strip()


def clean_and_chunk(transcript: dict, chunk_size: int = None, overlap: int = None) -> List[Dict]:
    """
    Clean segments and group them into overlapping word-count chunks.
    Returns list of {text, start_time, end_time, chunk_index}.
    """
    chunk_size = chunk_size or Config.CHUNK_SIZE
    overlap    = overlap    or Config.CHUNK_OVERLAP

    segments = transcript.get("segments", [])
    video_id = transcript.get("video_id", "unknown")

    # Clean every segment
    cleaned = []
    for seg in segments:
        text = clean_text(seg.get("text", ""))
        if text:
            cleaned.append({
                "text":     text,
                "start":    seg.get("start", 0),
                "duration": seg.get("duration", 0),
            })

    # Save cleaned transcript
    os.makedirs(Config.PROCESSED_DIR, exist_ok=True)
    cleaned_path = os.path.join(Config.PROCESSED_DIR, f"{video_id}_cleaned.json")
    with open(cleaned_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    # Sliding-window word chunking
    # Build word list with segment metadata
    words = []
    for seg in cleaned:
        for word in seg["text"].split():
            words.append({"word": word, "start": seg["start"],
                          "end": seg["start"] + seg["duration"]})

    chunks = []
    i = 0
    idx = 0
    while i < len(words):
        window = words[i : i + chunk_size]
        chunk_text = " ".join(w["word"] for w in window)
        chunks.append({
            "chunk_index": idx,
            "text":        chunk_text,
            "start_time":  window[0]["start"],
            "end_time":    window[-1]["end"],
            "video_id":    video_id,
        })
        idx += 1
        i   += chunk_size - overlap  # slide forward

    return chunks

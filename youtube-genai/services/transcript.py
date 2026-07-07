import os
import re
import json
from typing import Optional

from config import Config

try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        TranscriptsDisabled,
        NoTranscriptFound,
    )

    yt_api = YouTubeTranscriptApi()
    TRANSCRIPT_API_AVAILABLE = True

except ImportError:
    TRANSCRIPT_API_AVAILABLE = False


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID."""

    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_transcript(video_id: str):
    """
    Fetch transcript using youtube-transcript-api v1.x
    """

    if not TRANSCRIPT_API_AVAILABLE:
        raise RuntimeError(
            "youtube-transcript-api is not installed.\n"
            "Run: pip install youtube-transcript-api"
        )

    try:
        transcript = yt_api.fetch(video_id)

        return [
            {
                "text": item.text,
                "start": item.start,
                "duration": item.duration,
            }
            for item in transcript
        ]

    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video.")

    except NoTranscriptFound:
        raise ValueError("No transcript is available for this video.")

    except Exception as e:
        raise ValueError(f"Transcript extraction failed: {e}")


def save_transcript(data: list, video_id: str):
    os.makedirs(Config.TRANSCRIPTS_DIR, exist_ok=True)

    path = os.path.join(
        Config.TRANSCRIPTS_DIR,
        f"{video_id}.json",
    )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "video_id": video_id,
                "segments": data,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    return path


def load_transcript(video_id: str):
    path = os.path.join(
        Config.TRANSCRIPTS_DIR,
        f"{video_id}.json",
    )

    if not os.path.exists(path):
        return None

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_transcripts():
    result = []

    if not os.path.isdir(Config.TRANSCRIPTS_DIR):
        return result

    for filename in os.listdir(Config.TRANSCRIPTS_DIR):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(
            Config.TRANSCRIPTS_DIR,
            filename,
        )

        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)

            segments = data.get("segments", [])

            duration = 0

            if segments:
                duration = (
                    segments[-1]["start"]
                    + segments[-1]["duration"]
                )

            stat = os.stat(filepath)

            result.append(
                {
                    "video_id": filename[:-5],
                    "segments": len(segments),
                    "duration": int(duration),
                    "size_bytes": stat.st_size,
                    "modified": stat.st_mtime,
                }
            )

        except Exception:
            pass

    return result


def format_timestamp(seconds):
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"

    return f"{minutes:02}:{secs:02}"
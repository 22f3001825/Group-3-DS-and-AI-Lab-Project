import os
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse
import re

try:
    import whisper
    import yt_dlp
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: Whisper or yt-dlp not available. Fallback disabled.")

def extract_video_id(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            p = urllib.parse.parse_qs(parsed.query)
            return p['v'][0]
    return None

def format_timestamp(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_with_whisper(url):
    print(f"  -> Falling back to Whisper for {url}...")
    temp_audio = "temp_audio_w12_l4.m4a"
    download_audio(url, temp_audio)
    
    model = whisper.load_model("base")
    result = model.transcribe(temp_audio)
    
    transcript_text = ""
    for segment in result["segments"]:
        timestamp = format_timestamp(segment["start"])
        text = segment["text"].strip()
        transcript_text += f"\n(Refer Slide Time: {timestamp}) {text}\n"
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
        
    return transcript_text

def process_single(url, week_name, lecture_num):
    base_dir = Path(__file__).parent.parent / "data" / "raw" / "transcripts" / week_name
    base_dir.mkdir(parents=True, exist_ok=True)
    
    file_name = f"Lecture {lecture_num}.md"
    out_path = base_dir / file_name
    
    print(f"Processing {week_name} - Lecture {lecture_num}")
    video_id = extract_video_id(url)
    
    if not video_id:
        print(f"  -> Invalid URL: {url}")
        return
        
    try:
        api = YouTubeTranscriptApi()
        transcript = api.get_transcript(video_id)
        
        transcript_text = f"# {week_name} - Lecture {lecture_num}\n\n"
        for entry in transcript:
            timestamp = format_timestamp(entry['start'])
            text = entry['text'].strip()
            transcript_text += f"\n(Refer Slide Time: {timestamp}) {text}\n"
        
        out_path.write_text(transcript_text, encoding='utf-8')
        print(f"  -> Successfully extracted via API.")
        
    except Exception as e:
        print(f"  -> API failed: {e}")
        if WHISPER_AVAILABLE:
            try:
                transcript_text = f"# {week_name} - Lecture {lecture_num}\n\n"
                transcript_text += transcribe_with_whisper(url)
                out_path.write_text(transcript_text, encoding='utf-8')
                print(f"  -> Successfully extracted via Whisper.")
            except Exception as we:
                print(f"  -> Whisper failed: {we}")
        else:
            print("  -> Could not extract transcript (Whisper unavailable).")

if __name__ == "__main__":
    url = "https://youtu.be/Y6CNz0wRWpI?si=3eag04Hbn1Pkf4de"
    process_single(url, "Week-12", 4)

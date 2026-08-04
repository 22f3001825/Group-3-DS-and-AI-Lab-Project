import os
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse
import re

# Fallback tools
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
    # Format as MM:SS (which clean_dataset expects for Refer Slide Time)
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
    temp_audio = "temp_audio.m4a"
    download_audio(url, temp_audio)
    
    model = whisper.load_model("base")
    result = model.transcribe(temp_audio)
    
    transcript_text = ""
    for segment in result["segments"]:
        timestamp = format_timestamp(segment["start"])
        text = segment["text"].strip()
        # Using (Refer Slide Time: MM:SS) to match the regex in clean_dataset.py exactly
        transcript_text += f"\n(Refer Slide Time: {timestamp}) {text}\n"
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
        
    return transcript_text

def process_lectures(lectures, week_name):
    base_dir = Path(__file__).parent.parent / "data" / "raw" / "transcripts" / week_name
    base_dir.mkdir(parents=True, exist_ok=True)
    
    for i, url in enumerate(lectures, 1):
        file_name = f"Lecture {i}.md"
        out_path = base_dir / file_name
        
        print(f"Processing {week_name} - Lecture {i}")
        video_id = extract_video_id(url)
        
        if not video_id:
            print(f"  -> Invalid URL: {url}")
            continue
            
        try:
            # Try getting via API
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            transcript_text = f"# {week_name} - Lecture {i}\n\n"
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
                    transcript_text = f"# {week_name} - Lecture {i}\n\n"
                    transcript_text += transcribe_with_whisper(url)
                    out_path.write_text(transcript_text, encoding='utf-8')
                    print(f"  -> Successfully extracted via Whisper.")
                except Exception as we:
                    print(f"  -> Whisper failed: {we}")
            else:
                print("  -> Could not extract transcript (Whisper unavailable).")

if __name__ == "__main__":
    week9 = [
        "https://youtu.be/G7tYdl0Osf4?si=62Im-9F3QDn8X0_C",
        "https://youtu.be/FMRpmR9HNtY?si=1YbTw_vSRYPLKQBw",
        "https://youtu.be/fHDouTKwfXw?si=NPRrCaA5Ip7PoX3Q",
        "https://youtu.be/udFWtBLJUvA?si=POjW_qGs6KKRmuxL",
        "https://youtu.be/bb4yn4RssLs?si=ytop-bwsRXs7zU3z"
    ]
    
    week10 = [
        "https://youtu.be/-guLBqucS_I?si=qAj_cBDvcdCnt1EE",
        "https://youtu.be/ZzWFdt_6KLA?si=N7chWfzd5H1I4sCA",
        "https://youtu.be/7Th2YgPMnk0?si=KXp9uqY9-ozU4FWw",
        "https://youtu.be/85BxDKkiK4c?si=SgJFv-Y0qKqq7K3Y",
        "https://youtu.be/2LnQ2r7Q3-0?si=MtCMGUT6I21zdB1s",
        "https://youtu.be/leolYGmaFLM?si=pPIoi8BufHn1VCCU"
    ]
    
    week11 = [
        "https://youtu.be/MZzp4OP8GgQ?si=5pIon8m6OaO5yhV0",
        "https://youtu.be/jthjk2nboDM?si=QCCcXCtu2QnALL9q",
        "https://youtu.be/jbcaJ_kn3CQ?si=MFz3tUCkuaofVq1C",
        "https://youtu.be/VcrPtcJWvDE?si=wDCnZjOMhT8sFE6Q",
        "https://youtu.be/OXTu2vrsTjY?si=86lNu3qqmCOOcQvc",
        "https://youtu.be/-B534pLpnhk?si=Ud2Hz_z1NAna8zAt"
    ]
    
    week12 = [
        "https://youtu.be/1ok_K5EohoU?si=Ot4wUpGKJ34ouOdm",
        "https://youtu.be/tXVelGBsIPI?si=sg25tsTG9DSD53wY",
        "https://youtu.be/ZAuZqOM-skQ?si=1p56qwquMaukIrS8",
        "https://youtu.be/Y6CNz0wRWpI?si=IfHKQeev55LqcKZJ",
        "https://youtu.be/LctgFHD_RN4?si=C8tlSr8iU_0XQIW1",
        "https://youtu.be/06PP-3xUCs0?si=5tsSjiX5LEb91lpR"
    ]
    
    process_lectures(week9, "Week-9")
    process_lectures(week10, "Week-10")
    process_lectures(week11, "Week-11")
    process_lectures(week12, "Week-12")

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from services.transcript import fetch_transcript, save_transcript, extract_video_id

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET"])
@login_required
def index():
    return render_template("upload.html")


@upload_bp.route("/upload", methods=["POST"])
@login_required
def extract():
    url = request.form.get("youtube_url", "").strip()
    if not url:
        flash("Please enter a YouTube URL.", "danger")
        return redirect(url_for("upload.index"))

    video_id = extract_video_id(url)
    if not video_id:
        flash("Invalid YouTube URL. Please check and try again.", "danger")
        return redirect(url_for("upload.index"))

    try:
        transcript_data = fetch_transcript(video_id)
        filepath = save_transcript(transcript_data, video_id)
        flash(f"Transcript extracted successfully! ({len(transcript_data)} segments)", "success")
        return redirect(url_for("transcript.view", video_id=video_id))
    except Exception as e:
        flash(f"Failed to extract transcript: {str(e)}", "danger")
        return redirect(url_for("upload.index"))

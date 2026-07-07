from flask import Blueprint, render_template, abort
from flask_login import login_required
import os, json
from config import Config
from services.transcript import load_transcript, list_transcripts

transcript_bp = Blueprint("transcript", __name__)


@transcript_bp.route("/transcripts")
@login_required
def index():
    transcripts = list_transcripts()
    return render_template("transcript_list.html", transcripts=transcripts)


@transcript_bp.route("/transcript/<video_id>")
@login_required
def view(video_id):
    data = load_transcript(video_id)
    if data is None:
        abort(404)
    return render_template("transcript.html", transcript=data, video_id=video_id)

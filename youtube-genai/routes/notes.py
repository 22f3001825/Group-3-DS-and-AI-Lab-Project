import os
import re
import json
from flask import Blueprint, render_template, request, jsonify, send_file, abort
from flask_login import login_required
from config import Config
from services.notes_generator import generate_notes
from services.pdf_generator import create_pdf

notes_bp = Blueprint("notes", __name__)

_VALID_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_NOTES_CACHE_DIR = os.path.join(Config.PROCESSED_DIR, "notes_cache")


def _sanitize_video_id(video_id: str) -> str:
    """
    Reject anything that isn't a plain video ID before it ever touches a file
    path, so a crafted id (e.g. containing '../') can't escape the intended
    cache/export directories.
    """
    if not video_id or not _VALID_VIDEO_ID_RE.match(video_id):
        abort(400, description="Invalid video ID.")
    return video_id


def _load_transcript(video_id: str):
    """
    Load a transcript dict for video_id from Config.TRANSCRIPTS_DIR.
    Expects a file named "{video_id}.json" containing {"segments": [...]}.
    Returns None if no matching transcript exists.
    """
    path = os.path.join(Config.TRANSCRIPTS_DIR, f"{video_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _valid_mode(mode: str) -> str:
    return mode if mode in ("simple", "detailed") else "simple"


def _cache_path(video_id: str, mode: str) -> str:
    os.makedirs(_NOTES_CACHE_DIR, exist_ok=True)
    return os.path.join(_NOTES_CACHE_DIR, f"{video_id}_{mode}_notes.json")


def _get_notes(video_id: str, mode: str, force_refresh: bool = False) -> dict:
    """
    Return generated notes for (video_id, mode), reusing a cached copy on disk
    whenever possible so repeat page views and PDF downloads don't re-run the
    LLM from scratch every time (each call is several sequential Ollama
    requests, one per section).

    Pass force_refresh=True (e.g. via ?refresh=1) to bypass the cache and
    regenerate notes fresh, overwriting the cached copy.
    """
    cache_file = _cache_path(video_id, mode)

    if not force_refresh and os.path.exists(cache_file):
        try:
            with open(cache_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass  # cache file is corrupt/unreadable — fall through and regenerate

    transcript = _load_transcript(video_id)
    if transcript is None:
        abort(404, description=f"No transcript found for video '{video_id}'. Process it first.")

    notes = generate_notes(transcript, video_id, detail_level=mode)

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # caching is best-effort; don't fail the request just because saving failed

    return notes


@notes_bp.route("/notes")
@login_required
def index():
    return render_template("notes.html")


@notes_bp.route("/notes/<video_id>")
@login_required
def view(video_id):
    """
    Render explanation-style notes for a given video at the requested detail level.
    e.g. /notes/<video_id>?mode=detailed
    Add &refresh=1 to force regenerating instead of using the cached copy.
    """
    video_id = _sanitize_video_id(video_id)
    mode = _valid_mode(request.args.get("mode", "simple"))
    force_refresh = request.args.get("refresh") == "1"

    notes = _get_notes(video_id, mode, force_refresh=force_refresh)
    return render_template("notes.html", notes=notes, video_id=video_id, mode=mode)


@notes_bp.route("/notes/<video_id>/pdf")
@login_required
def download_pdf(video_id):
    """
    Stream generated notes back as a PDF download, reusing cached notes when
    available (e.g. if the user already viewed this video/mode on the page).
    e.g. /notes/<video_id>/pdf?mode=detailed
    """
    video_id = _sanitize_video_id(video_id)
    mode = _valid_mode(request.args.get("mode", "simple"))
    force_refresh = request.args.get("refresh") == "1"

    notes = _get_notes(video_id, mode, force_refresh=force_refresh)

    export_dir = os.path.join(Config.PROCESSED_DIR, "pdf_exports")
    os.makedirs(export_dir, exist_ok=True)
    output_path = os.path.join(export_dir, f"{video_id}_{mode}_notes.pdf")

    create_pdf(notes, output_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"{video_id}_{mode}_notes.pdf",
        mimetype="application/pdf",
    )
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os, json
from config import Config

dashboard_bp = Blueprint("dashboard", __name__)


def _count_transcripts():
    d = Config.TRANSCRIPTS_DIR
    if not os.path.isdir(d):
        return 0
    return len([f for f in os.listdir(d) if f.endswith(".json")])


def _count_chunks():
    d = Config.PROCESSED_DIR
    total = 0
    if not os.path.isdir(d):
        return 0
    for f in os.listdir(d):
        if f.endswith("_chunks.json"):
            try:
                with open(os.path.join(d, f)) as fp:
                    total += len(json.load(fp))
            except Exception:
                pass
    return total


def _vector_db_status():
    index_path = os.path.join(Config.VECTOR_DB_DIR, "index.faiss")
    return "Ready ✔" if os.path.exists(index_path) else "Not built"


@dashboard_bp.route("/dashboard")
@login_required
def index():
    stats = {
        "transcripts": _count_transcripts(),
        "chunks":      _count_chunks(),
        "vector_db":   _vector_db_status(),
    }
    return render_template("dashboard.html", stats=stats)

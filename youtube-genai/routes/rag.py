from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from services.rag_pipeline import answer_question
from services.vectorstore import get_index_stats

rag_bp = Blueprint("rag", __name__)


@rag_bp.route("/rag")
@login_required
def index():
    return render_template("rag.html")


@rag_bp.route("/rag/videos", methods=["GET"])
@login_required
def videos():
    """Return the list of currently indexed video_ids, for the video-scope dropdown."""
    stats = get_index_stats()
    return jsonify({"videos": stats.get("videos", [])})


@rag_bp.route("/rag/ask", methods=["POST"])
@login_required
def ask():
    data     = request.get_json(silent=True) or {}
    query    = data.get("query", "").strip()
    video_id = (data.get("video_id") or "").strip() or None

    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        result = answer_question(query, video_id=video_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
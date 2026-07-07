from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
import os, json
from config import Config
from services.transcript import load_transcript, list_transcripts
from services.preprocess  import clean_and_chunk
from services.embeddings  import embed_chunks
from services.vectorstore import build_index

dataset_bp = Blueprint("dataset", __name__)


def _pipeline_status(video_id: str) -> dict:
    """Return which pipeline steps are complete for a given video."""
    proc_dir = Config.PROCESSED_DIR
    return {
        "raw":        os.path.exists(os.path.join(Config.TRANSCRIPTS_DIR, f"{video_id}.json")),
        "cleaned":    os.path.exists(os.path.join(proc_dir, f"{video_id}_cleaned.json")),
        "chunks":     os.path.exists(os.path.join(proc_dir, f"{video_id}_chunks.json")),
        "embeddings": os.path.exists(os.path.join(proc_dir, f"{video_id}_embeddings.npy")),
        "faiss":      os.path.exists(os.path.join(Config.VECTOR_DB_DIR, "index.faiss")),
    }


@dataset_bp.route("/dataset")
@login_required
def index():
    transcripts = list_transcripts()
    return render_template("dataset.html", transcripts=transcripts)


@dataset_bp.route("/dataset/<video_id>")
@login_required
def detail(video_id):
    status = _pipeline_status(video_id)
    return render_template("dataset_detail.html", video_id=video_id, status=status)


@dataset_bp.route("/dataset/process/<video_id>", methods=["POST"])
@login_required
def process(video_id):
    """Run the full preprocessing pipeline for a transcript."""
    try:
        raw = load_transcript(video_id)
        if raw is None:
            return jsonify({"error": "Transcript not found"}), 404

        # Step 1: Clean + Chunk
        chunks = clean_and_chunk(raw)
        chunk_path = os.path.join(Config.PROCESSED_DIR, f"{video_id}_chunks.json")
        with open(chunk_path, "w") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        # Step 2: Embed
        embeddings = embed_chunks([c["text"] for c in chunks])
        import numpy as np
        emb_path = os.path.join(Config.PROCESSED_DIR, f"{video_id}_embeddings.npy")
        np.save(emb_path, embeddings)

        # Step 3: Build / update FAISS index
        build_index(embeddings, chunks, video_id)

        return jsonify({
            "status": "success",
            "chunks": len(chunks),
            "pipeline": _pipeline_status(video_id)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dataset_bp.route("/dataset/status/<video_id>")
@login_required
def status(video_id):
    return jsonify(_pipeline_status(video_id))

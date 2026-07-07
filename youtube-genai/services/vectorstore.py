"""
services/vectorstore.py
────────────────────────────────────────────────────────────
Manages the FAISS index and metadata store.
Supports building from scratch and incremental additions.

Multi-video support:
  Each video's embeddings are saved as {video_id}_embeddings.npy in
  PROCESSED_DIR (done by dataset.py before calling build_index).
  build_index() loads ALL existing videos' .npy files plus the new one,
  so the FAISS index always contains every processed video's chunks.
"""

import os
import json
import pickle
import numpy as np
from config import Config

_INDEX_PATH    = os.path.join(Config.VECTOR_DB_DIR, "index.faiss")
_METADATA_PATH = os.path.join(Config.VECTOR_DB_DIR, "metadata.pkl")

_index    = None
_metadata = []   # list of chunk dicts (parallel to index rows)


def _ensure_dir():
    os.makedirs(Config.VECTOR_DB_DIR, exist_ok=True)
    os.makedirs(Config.PROCESSED_DIR, exist_ok=True)


def build_index(embeddings: np.ndarray, chunks: list, video_id: str):
    """
    Build or update the FAISS flat inner-product index.
    Since embeddings are L2-normalised, inner product == cosine similarity.

    Strategy:
      1. Save the current video's embeddings to disk (idempotent).
      2. Load ALL per-video .npy files from PROCESSED_DIR.
      3. Rebuild the full FAISS index from scratch using all videos.
    """
    global _index, _metadata

    try:
        import faiss
    except ImportError:
        raise RuntimeError("faiss-cpu not installed. Run: pip install faiss-cpu")

    _ensure_dir()

    # ── Step 1: persist this video's embeddings ──────────────────────────────
    emb_path = os.path.join(Config.PROCESSED_DIR, f"{video_id}_embeddings.npy")
    np.save(emb_path, embeddings)

    # Persist this video's chunk metadata alongside
    chunk_path = os.path.join(Config.PROCESSED_DIR, f"{video_id}_chunks.json")
    if not os.path.exists(chunk_path):
        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    # ── Step 2: discover every video with a saved .npy file ─────────────────
    all_embs_list  = []
    all_chunks_list = []

    npy_files = [
        fn for fn in os.listdir(Config.PROCESSED_DIR)
        if fn.endswith("_embeddings.npy")
    ]

    for npy_fn in sorted(npy_files):
        vid = npy_fn[: -len("_embeddings.npy")]
        npy_full   = os.path.join(Config.PROCESSED_DIR, npy_fn)
        chunk_full = os.path.join(Config.PROCESSED_DIR, f"{vid}_chunks.json")

        try:
            emb = np.load(npy_full).astype("float32")

            if os.path.exists(chunk_full):
                with open(chunk_full, encoding="utf-8") as f:
                    vid_chunks = json.load(f)
            else:
                # Fallback: use the freshly provided chunks for the current video
                if vid == video_id:
                    vid_chunks = chunks
                else:
                    # No chunk metadata → skip this video to keep index consistent
                    print(f"[vectorstore] Skipping {vid}: no chunk metadata found.")
                    continue

            # Guard: number of embeddings must match number of chunks
            if len(emb) != len(vid_chunks):
                print(
                    f"[vectorstore] Dimension mismatch for {vid} "
                    f"(embs={len(emb)}, chunks={len(vid_chunks)}). Skipping."
                )
                continue

            all_embs_list.append(emb)
            all_chunks_list.extend(vid_chunks)

        except Exception as exc:
            print(f"[vectorstore] Error loading {vid}: {exc}. Skipping.")
            continue

    if not all_embs_list:
        print("[vectorstore] No valid embeddings found. Index not built.")
        return

    all_embs = np.vstack(all_embs_list).astype("float32")

    # ── Step 3: rebuild FAISS index ──────────────────────────────────────────
    dim       = all_embs.shape[1]
    new_index = faiss.IndexFlatIP(dim)
    new_index.add(all_embs)

    faiss.write_index(new_index, _INDEX_PATH)
    with open(_METADATA_PATH, "wb") as f:
        pickle.dump(all_chunks_list, f)

    _index    = new_index
    _metadata = all_chunks_list

    indexed_videos = list({c.get("video_id", "?") for c in all_chunks_list})
    print(
        f"[vectorstore] Index built: {new_index.ntotal} vectors "
        f"from {len(indexed_videos)} video(s): {indexed_videos}"
    )


def search(query_vector: np.ndarray, top_k: int = 5, video_id: str = None) -> list:
    """
    Search the FAISS index. Returns top_k chunk dicts with score.

    If `video_id` is provided, results are restricted to chunks belonging to
    that video only. Since the FAISS index is a single flat index spanning
    all videos, we over-fetch a larger candidate pool and filter by
    video_id afterward, then trim back down to top_k.
    """
    global _index, _metadata

    try:
        import faiss
    except ImportError:
        raise RuntimeError("faiss-cpu not installed.")

    # Lazy load
    if _index is None:
        if os.path.exists(_INDEX_PATH):
            _index = faiss.read_index(_INDEX_PATH)
            with open(_METADATA_PATH, "rb") as f:
                _metadata = pickle.load(f)
        else:
            return []

    if _index.ntotal == 0:
        return []

    if video_id:
        # Over-fetch: search the whole index (or a generous cap) so we have
        # enough same-video candidates to fill top_k after filtering.
        fetch_k = min(_index.ntotal, max(top_k * 20, 200))
        scores, indices = _index.search(query_vector, fetch_k)
    else:
        scores, indices = _index.search(query_vector, min(top_k, _index.ntotal))

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(_metadata):
            continue
        chunk = dict(_metadata[idx])
        if video_id and chunk.get("video_id") != video_id:
            continue
        chunk["score"] = float(score)
        results.append(chunk)
        if len(results) >= top_k:
            break
    return results


def get_index_stats() -> dict:
    """Return basic stats about the current FAISS index."""
    if os.path.exists(_INDEX_PATH) and os.path.exists(_METADATA_PATH):
        try:
            import faiss
            idx = faiss.read_index(_INDEX_PATH)
            with open(_METADATA_PATH, "rb") as f:
                meta = pickle.load(f)
            videos = list({m.get("video_id", "?") for m in meta})
            return {"total_chunks": idx.ntotal, "videos": videos, "ready": True}
        except Exception:
            pass
    return {"total_chunks": 0, "videos": [], "ready": False}
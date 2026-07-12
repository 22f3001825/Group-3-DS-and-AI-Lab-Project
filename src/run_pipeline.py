"""Run the local forum cleaning, chunking, evaluation, and Qdrant ingestion stages."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import requests


ROOT_DIR = Path(__file__).resolve().parent.parent


def wait_for_qdrant(url: str, attempts: int = 60, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=3)
            if response.ok:
                print(f"Qdrant is reachable at {url}.")
                return
        except requests.RequestException:
            pass
        print(f"Waiting for Qdrant ({attempt}/{attempts})...")
        time.sleep(delay_seconds)
    raise RuntimeError(f"Qdrant did not become reachable at {url}.")


def run(command: list[str]) -> None:
    print("Running:", " ".join(command))
    subprocess.run(command, cwd=ROOT_DIR, check=True)


def main() -> None:
    qdrant_url = os.environ.get("QDRANT_URL", "http://qdrant:6333")
    export_path = Path(os.environ.get("DISCOURSE_EXPORT_PATH", "/input/discourse_export.json"))
    if not export_path.exists():
        raise FileNotFoundError(
            f"Discourse export not found at {export_path}. "
            "Mount it into the pipeline container or set DISCOURSE_EXPORT_PATH."
        )

    wait_for_qdrant(qdrant_url)
    run([sys.executable, "src/clean_discourse_export.py", "--input", str(export_path)])
    run([sys.executable, "src/prepare_rag_splits.py"])
    run([sys.executable, "src/build_discourse_evaluation.py"])
    ingest_command = [sys.executable, "src/ingest_to_qdrant.py"]
    if os.environ.get("RECREATE_COLLECTION", "").lower() in {"1", "true", "yes"}:
        ingest_command.append("--recreate")
    run(ingest_command)


if __name__ == "__main__":
    main()

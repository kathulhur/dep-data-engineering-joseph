from typing import Literal
from pathlib import Path
import requests
"""
Phase 2 — Data Ingestion
Replace this template with your own ingestion logic.
"""

import os

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def ingest(
        type: Literal["posts", "comments"], 
        source='https://raw.githubusercontent.com/kathulhur/dep-data-engineering-joseph/main/data/raw/',
        dest_dir=Path().cwd() / 'data' / 'raw'
    ):
    assert type is not None
    assert type == 'posts' or type == 'comments'
    filename = type + '.json'
    url = source + filename
    resp = requests.get(url)
    
    resp.raise_for_status()
    dest_path = dest_dir / filename
    with dest_path.open("wb") as f:
        f.write(resp.content)

if __name__ == "__main__":
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    ingest("posts")
    ingest("comments")
    print("Ingestion complete. Check data/raw/ for output.")

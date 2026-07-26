from __future__ import annotations

from pathlib import Path
from uuid import uuid4

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"


def save_uploaded_image(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Only PNG, JPG, JPEG, and WEBP images are supported.")

    filename = f"{uuid4().hex}{extension}"
    target = UPLOAD_DIR / filename
    target.write_bytes(uploaded_file.getbuffer())

    return str(target)

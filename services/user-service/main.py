import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from app.main import app  # noqa: E402,F401

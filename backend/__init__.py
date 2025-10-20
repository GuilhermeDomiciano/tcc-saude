"""
Make backend an importable package and provide a compatibility alias so
imports like `from app.core import ...` work whether the app is executed
from the repo root (backend.main) or from inside the backend folder.
"""

import sys
import importlib

try:
    # Map top-level name 'app' to this package's subpackage 'backend.app'
    if 'app' not in sys.modules:
        sys.modules['app'] = importlib.import_module(__name__ + '.app')
except Exception:
    # Best-effort; tests/dev shouldn't break if alias fails
    pass

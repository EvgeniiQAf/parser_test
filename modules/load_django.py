"""Load Django environment for external scripts and parsers."""

import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")
django.setup()

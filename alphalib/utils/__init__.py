from pathlib import Path

from .dateutils import *
from .logger import *


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

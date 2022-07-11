import re

from .dateutils import *
from .logger import *


def sanitized_column_name(name: str):
    """Sanitize the column name.

    Args:
        name (string): Column name.

    Returns:
        A valid column name.
    """
    if not name:
        raise ValueError("Name cannot be empty")
    name = re.sub(r"[\s().\-/]+", "_", name.lower())
    name = re.sub(r"(^\d)", r"_\1", name)
    name = name.removesuffix("_")
    return name

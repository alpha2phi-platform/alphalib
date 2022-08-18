import dataclasses
import json
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, List, Optional, Tuple


def json_encoder(cls):
    def decimal_to_float_factory(data: List[Tuple[str, Any]]):
        """Decimal to float factory

        Convert decimal to float.

        Args:
            data: List of tuples.
        """
        return {
            field: float(value) if isinstance(value, Decimal) else value
            for field, value in data
        }

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return asdict(o, dict_factory=decimal_to_float_factory)
            return super().default(o)

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder)

    cls.to_json = to_json
    return cls


@dataclass
@json_encoder
class Stock:
    """
    Stock class.
    """

    name: str
    symbol: str
    sector: str
    country: str
    eps: float
    trailing_pe: float
    forward_pe: float

import dataclasses
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, List, Tuple

from ..utils import dateutils


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
    Stock class
    """

    symbol: str
    name: str
    full_name: str
    currency: str
    country: str
    isin: str
    update_datetime: Decimal
    update_datetime_isoformat: str

    info_update_datetime: Decimal = Decimal(dateutils.to_epoch_time(datetime.min))
    info_update_datetime_isoformat: str = dateutils.to_isoformat(datetime.min)

    # def __setattr__(self, prop, val):
    # if val is not None and (
    #     prop == "update_datetime" or prop == "info_update_datetime"
    # ):
    #     super().__setattr__(prop, Decimal(val))
    # super().__setattr__(prop, val)


# TODO: Add more fields
@dataclass
class StockInfo:
    """
    Stock info class
    """


# TODO: Add more fields
@dataclass
class StockDividend:
    """
    Stock dividend class
    """

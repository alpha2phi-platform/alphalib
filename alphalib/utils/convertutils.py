from dataclasses import asdict
from datetime import datetime

import pandas as pd


class TypeConverter(object):
    def to_df(self):
        """Convert dataclass to Pandas data frame.

        Returns:
            Pandas data frame.
        """
        return pd.DataFrame(
            [
                asdict(
                    self,
                    dict_factory=lambda x: {
                        k: v
                        for (k, v) in x
                        if (type(v) is not pd.DataFrame and type(v) is not pd.Series)
                    },
                )
            ]
        )


def strip(text) -> str:
    if text:
        return text.strip()
    return ""


def to_date(text, format="%m/%d/%Y") -> datetime:
    if text:
        try:
            return datetime.strptime(strip(text), format)
        except Exception:
            return datetime.min
    return datetime.min


def strip_chars(text, chars=" $%\xa0") -> str:
    if text:
        return text.strip(chars)
    return ""


def dt_from_ts(text) -> datetime:
    if text:
        try:
            return datetime.fromtimestamp(text)
        except Exception:
            return datetime.min
    return datetime.min


def to_float(text: str) -> float:
    if text:
        try:
            return float(strip_chars(text))
        except Exception:
            return 0
    return 0


def join_dicts(to_dict, from_dict, from_dict_key) -> dict:
    if from_dict[from_dict_key]:
        v = from_dict[from_dict_key]
        if type(v) is dict:
            to_dict = {**to_dict, **v}
        return to_dict
    return to_dict


def set_fields(fr, to):
    for key, value in asdict(fr).items():
        setattr(to, key, value)


def none_if_not_avail(val):
    if val in ["N/A", "NA"]:
        return None
    return val

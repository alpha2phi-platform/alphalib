from datetime import datetime


def strip(text):
    if text:
        return text.strip()
    return ""


def to_date(text, format="%m/%d/%Y"):
    if text:
        try:
            return datetime.strptime(strip(text), format)
        except Exception:
            return datetime.min
    return datetime.min


def strip_chars(text, chars=" $%\xa0"):
    if text:
        return text.strip(chars)
    return ""


def to_float(text):
    if text:
        try:
            return float(strip_chars(text))
        except Exception:
            return 0
    return 0

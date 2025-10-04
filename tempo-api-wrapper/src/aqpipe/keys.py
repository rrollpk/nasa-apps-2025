import re, unicodedata

_ws = re.compile(r"\s+")


def strip_accents(s: str) -> str:
    if s is None:
        return " "
    # NFKD then drop combining marks (á -> a, ñ -> n)
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def norm(s: str) -> str:
    s = strip_accents((s or "").strip().lower())
    return _ws.sub(" ", s)  # collapse whitespace


def make_key(comunidad: str, provincia: str, poblacion: str) -> str:
    """Normalized composite key: comunidad|provincia|poblacion"""
    return f"{norm(comunidad)}|{norm(provincia)}|{norm(poblacion)}"

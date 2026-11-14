"""Stateless text normalization and preview formatting helpers."""
import re

_PREFIX_RE = re.compile(r"^(?:\s*(?:re|fwd|fw)\s*:\s*)+", re.IGNORECASE)
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_subject(subject: str) -> str:
    """Strip reply/forward prefixes and normalize whitespace."""
    cleaned = _PREFIX_RE.sub("", subject or "")
    return _WHITESPACE_RE.sub(" ", cleaned).strip()


def truncate_preview(body: str, max_length: int = 160) -> str:
    """Return a clean single-line preview bounded to max_length."""
    compact = _WHITESPACE_RE.sub(" ", (body or "").strip())
    if len(compact) <= max_length:
        return compact
    return compact[: max(0, max_length - 3)].rstrip() + "..."

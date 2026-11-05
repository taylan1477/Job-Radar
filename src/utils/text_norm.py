def normalize_tr(s: str) -> str:
    """Türkçe karakterleri güvenli şekilde normalize eder (İ -> i, I -> ı)."""
    if not s:
        return ""
    return s.replace("İ", "i").replace("I", "ı").lower()

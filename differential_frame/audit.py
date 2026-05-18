"""
Batch audit tool. Scans a file or string for in-frame /
out-of-frame claims. Designed to run on a phone in <1s
for typical README-sized inputs.
"""
from .validators import quick_audit


def audit_text(text: str, min_sentence_len: int = 20) -> list:
    """
    Returns list of dicts: one per sentence, with frame check.
    """
    # crude sentence split — stdlib only, no nltk
    sentences = []
    buf = []
    for ch in text:
        buf.append(ch)
        if ch in '.!?\n':
            s = ''.join(buf).strip()
            if len(s) >= min_sentence_len:
                sentences.append(s)
            buf = []
    if buf:
        s = ''.join(buf).strip()
        if len(s) >= min_sentence_len:
            sentences.append(s)

    return [
        {'sentence': s, **quick_audit(s)}
        for s in sentences
    ]


def audit_file(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return audit_text(f.read())


def summarize(results: list) -> dict:
    total = len(results)
    passing = sum(1 for r in results if r['in_frame'])
    drift = sum(1 for r in results if r['has_drift'])
    return {
        'total_claims':  total,
        'in_frame':      passing,
        'out_of_frame':  total - passing,
        'drift_flagged': drift,
        'frame_rate':    (passing / total) if total else 1.0,
    }

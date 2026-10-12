from __future__ import annotations
import os
import json
import re
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_data")
os.makedirs(DATA_DIR, exist_ok=True)

# RAGP thresholds
def score_to_status(pct: int) -> str:
    if pct == 100:    return "pink"
    elif pct >= 70:   return "green"
    elif pct >= 50:   return "amber"
    else:             return "red"


def _safe_key(username: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", username)


def _path(username: str) -> str:
    return os.path.join(DATA_DIR, f"{_safe_key(username)}.json")


def _load(username: str) -> dict:
    p = _path(username)
    if os.path.exists(p):
        with open(p, "r") as f:
            return json.load(f)
    return {"username": username, "progress": {}}


def _save(username: str, data: dict):
    with open(_path(username), "w") as f:
        json.dump(data, f, indent=2)


# ── Public API ────────────────────────────────────────────────────────────────

def get_lesson_progress(username: str, subject_key: str, lesson_id: str) -> dict | None:
    """Returns progress record for a lesson, or None if not attempted."""
    data = _load(username)
    return data.get("progress", {}).get(subject_key, {}).get(lesson_id)


def save_lesson_result(username: str, subject_key: str, lesson_id: str,
                       score: int, total: int):
    """Persist quiz result for a lesson."""
    data = _load(username)
    data.setdefault("progress", {}).setdefault(subject_key, {})
    pct = round(score / total * 100) if total else 0
    status = score_to_status(pct)
    existing = data["progress"][subject_key].get(lesson_id, {})
    best_pct = max(existing.get("best_pct", 0), pct)
    data["progress"][subject_key][lesson_id] = {
        "score": score,
        "total": total,
        "pct": pct,
        "best_pct": best_pct,
        "status": score_to_status(best_pct),
        "attempts": existing.get("attempts", 0) + 1,
        "last_date": str(date.today()),
    }
    _save(username, data)


def get_subject_stats(username: str, subject_key: str, all_lesson_ids: list[str]) -> dict:
    """Compute stats for a subject given a list of all lesson IDs."""
    data = _load(username)
    subj = data.get("progress", {}).get(subject_key, {})
    total = len(all_lesson_ids)
    completed = sum(1 for lid in all_lesson_ids if lid in subj)
    counts = {"red": 0, "amber": 0, "green": 0, "pink": 0}
    scores = []
    for lid in all_lesson_ids:
        if lid in subj:
            s = subj[lid].get("status", "red")
            counts[s] = counts.get(s, 0) + 1
            scores.append(subj[lid].get("best_pct", 0))
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    completion_pct = round(completed / total * 100) if total else 0
    return {
        "total": total,
        "completed": completed,
        "completion_pct": completion_pct,
        "avg_score": avg_score,
        "counts": counts,
    }


def get_category_status(username: str, subject_key: str, lesson_ids: list[str]) -> str:
    """Return RAGP status for a category (average of completed lessons)."""
    data = _load(username)
    subj = data.get("progress", {}).get(subject_key, {})
    pcts = [subj[lid]["best_pct"] for lid in lesson_ids if lid in subj]
    if not pcts:
        return "none"
    avg = round(sum(pcts) / len(pcts))
    return score_to_status(avg)

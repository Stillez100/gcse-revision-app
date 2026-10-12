from __future__ import annotations
import os
import json

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "curriculum_data")

SUBJECT_FILES = {
    "maths":   "maths_edexcel.json",
    "biology": "biology_aqa.json",
}

_cache: dict = {}


def load_subject(subject_key: str) -> dict:
    """Load a subject curriculum. Returns {} on failure."""
    if subject_key in _cache:
        return _cache[subject_key]
    fname = SUBJECT_FILES.get(subject_key, "")
    path = os.path.join(CURRICULUM_DIR, fname)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _cache[subject_key] = data
    return data


def get_all_subjects() -> list[dict]:
    """Return list of {key, subject, exam_board, icon} for every available subject."""
    result = []
    for key, fname in SUBJECT_FILES.items():
        path = os.path.join(CURRICULUM_DIR, fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            result.append({
                "key": key,
                "subject": d.get("subject", key.title()),
                "exam_board": d.get("exam_board", ""),
                "icon": d.get("icon", "📚"),
                "subject_code": d.get("subject_code", ""),
            })
    return result


def get_all_lessons(subject_key: str) -> list[dict]:
    """Flat list of all lessons across all categories."""
    data = load_subject(subject_key)
    lessons = []
    for cat in data.get("categories", []):
        for lesson in cat.get("lessons", []):
            lesson["category_id"] = cat["id"]
            lesson["category_title"] = cat["title"]
            lessons.append(lesson)
    return lessons


def get_lesson(subject_key: str, lesson_id: str) -> dict | None:
    """Find a single lesson by ID."""
    for lesson in get_all_lessons(subject_key):
        if lesson["id"] == lesson_id:
            return lesson
    return None

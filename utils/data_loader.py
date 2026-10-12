import os
import json
import streamlit as st
from typing import Dict, List, Any, Optional

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "curriculum_data")

def load_all_curricula() -> Dict[str, Dict[str, Any]]:
    curricula = {}
    if not os.path.exists(CURRICULUM_DIR):
        return curricula

    for fname in sorted(os.listdir(CURRICULUM_DIR)):
        if fname.endswith(".json"):
            fpath = os.path.join(CURRICULUM_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    subject_key = data.get("subject", fname.replace(".json", "").title())
                    curricula[subject_key] = data
            except Exception as e:
                st.error(f"Error loading {fname}: {e}")
    return curricula

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_data")
os.makedirs(USER_DATA_DIR, exist_ok=True)

def _get_user_progress_file():
    username = st.session_state.get("username", "guest")
    return os.path.join(USER_DATA_DIR, f"{username}_progress.json")

def init_user_progress():
    if "user_progress" not in st.session_state:
        filepath = _get_user_progress_file()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    st.session_state["user_progress"] = json.load(f)
            except Exception:
                st.session_state["user_progress"] = {}
        else:
            st.session_state["user_progress"] = {}
            
    if "question_submissions" not in st.session_state:
        st.session_state["question_submissions"] = {}

def save_user_progress():
    filepath = _get_user_progress_file()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(st.session_state.get("user_progress", {}), f, indent=4)
    except Exception as e:
        print(f"Failed to save progress: {e}")

from datetime import datetime

def get_ragp_color(pct: float) -> str:
    if pct == 100: return "Pink"
    if pct >= 70: return "Green"
    if pct >= 50: return "Amber"
    return "Red"

def get_topic_progress(topic_id: str) -> dict:
    init_user_progress()
    return st.session_state["user_progress"].get(topic_id, {"score": None, "color": "None", "completed": False})

def update_topic_quiz_score(topic_id: str, pct: float):
    init_user_progress()
    now_iso = datetime.now().isoformat()
    if topic_id not in st.session_state["user_progress"]:
        st.session_state["user_progress"][topic_id] = {}
    
    topic_data = st.session_state["user_progress"][topic_id]
    current_best = topic_data.get("score")
    
    topic_data["last_score"] = pct
    topic_data["last_attempted_at"] = now_iso
    
    if current_best is None or pct > current_best:
        topic_data["score"] = pct
        topic_data["color"] = get_ragp_color(pct)
        topic_data["completed"] = True
    else:
        topic_data.setdefault("completed", True)
        
    if "_attempt_history" not in st.session_state["user_progress"] or not isinstance(st.session_state["user_progress"]["_attempt_history"], list):
        st.session_state["user_progress"]["_attempt_history"] = []
        
    st.session_state["user_progress"]["_attempt_history"].append({
        "topic_id": topic_id,
        "score": pct,
        "color": get_ragp_color(pct),
        "timestamp": now_iso
    })
    
    save_user_progress()

def calculate_overall_stats(curricula: Dict[str, Dict[str, Any]]) -> dict:
    init_user_progress()
    progress = st.session_state.get("user_progress", {})
    
    stats = {
        "total_topics": 0,
        "completed": 0,
        "Red": 0,
        "Amber": 0,
        "Green": 0,
        "Pink": 0,
        "None": 0,
        "avg_score": None
    }
    
    all_scores = []
    for subj_data in curricula.values():
        stats["total_topics"] += len(subj_data.get("topics", []))

    for k, v in progress.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and v.get("completed"):
            stats["completed"] += 1
            if v.get("score") is not None:
                all_scores.append(v["score"])
            color = v.get("color", "Red")
            if color in stats:
                stats[color] += 1
                
    stats["None"] = max(0, stats["total_topics"] - stats["completed"])
    stats["completion_pct"] = round((stats["completed"] / max(1, stats["total_topics"])) * 100, 1)
    if all_scores:
        stats["avg_score"] = round(sum(all_scores) / len(all_scores))
    return stats

def calculate_subject_stats(subject_data: dict) -> dict:
    init_user_progress()
    topics = subject_data.get("topics", [])
    total = len(topics)
    completed = 0
    scores = []
    ragp = {"Pink": 0, "Green": 0, "Amber": 0, "Red": 0, "None": 0}
    
    for t in topics:
        prog = get_topic_progress(t["id"])
        if prog.get("completed"):
            completed += 1
            if prog.get("score") is not None:
                scores.append(prog["score"])
            color = prog.get("color", "Red")
            if color in ragp:
                ragp[color] += 1
        else:
            ragp["None"] += 1
            
    pct = round((completed / max(1, total)) * 100, 1)
    avg = round(sum(scores) / len(scores)) if scores else None
    return {
        "total": total,
        "completed": completed,
        "completion_pct": pct,
        "scores": scores,
        "avg_score": avg,
        "ragp": ragp
    }

def get_recent_subject_attempts(subject_data: dict, limit: int = 3) -> list:
    init_user_progress()
    progress = st.session_state.get("user_progress", {})
    topics_by_id = {t["id"]: t for t in subject_data.get("topics", [])}
    
    attempts = []
    history = progress.get("_attempt_history", [])
    if isinstance(history, list) and history:
        seen_topic_ids = set()
        for item in reversed(history):
            t_id = item.get("topic_id")
            if t_id in topics_by_id and t_id not in seen_topic_ids:
                topic_info = topics_by_id[t_id]
                seen_topic_ids.add(t_id)
                attempts.append({
                    "id": t_id,
                    "title": topic_info.get("title", t_id),
                    "category": topic_info.get("category", ""),
                    "tier": topic_info.get("tier", "Foundation / Higher"),
                    "score": item.get("score"),
                    "color": item.get("color", get_ragp_color(item.get("score", 0))),
                    "timestamp": item.get("timestamp")
                })
                if len(attempts) >= limit:
                    break
                    
    if len(attempts) < limit:
        for t_id, t_info in topics_by_id.items():
            if t_id not in [a["id"] for a in attempts]:
                t_prog = progress.get(t_id, {})
                if isinstance(t_prog, dict) and t_prog.get("completed") and t_prog.get("score") is not None:
                    attempts.append({
                        "id": t_id,
                        "title": t_info.get("title", t_id),
                        "category": t_info.get("category", ""),
                        "tier": t_info.get("tier", "Foundation / Higher"),
                        "score": t_prog.get("score"),
                        "color": t_prog.get("color", "Green"),
                        "timestamp": t_prog.get("last_attempted_at")
                    })
                    if len(attempts) >= limit:
                        break
                        
    return attempts

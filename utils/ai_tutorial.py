from __future__ import annotations
import os
import json
import base64
import time
import urllib.request
import urllib.error
from typing import Optional, List

CANDIDATE_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-3.1-flash-lite"
]

def get_api_key() -> Optional[str]:
    """Return Gemini API key from environment, Streamlit session state, or .env file."""
    # 1. Direct environment variable
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ.get("GOOGLE_API_KEY").strip()
    
    # 2. Streamlit secrets or session state
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            return str(st.secrets["GOOGLE_API_KEY"]).strip()
        if st.session_state.get("gemini_api_key"):
            return str(st.session_state.get("gemini_api_key")).strip()
    except Exception:
        pass

    # 3. Read .env file from app root
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GOOGLE_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            os.environ["GOOGLE_API_KEY"] = key
                            return key
        except Exception:
            pass

    return None


def generate_solution(question: str, marks: int, subject: str, image_file=None) -> str:
    """
    Call Google Gemini to generate a step-by-step GCSE model answer.
    Supports text and image questions with automatic active model fallback.
    """
    api_key = get_api_key()
    if not api_key:
        return (
            "⚠️ **Gemini API Key Missing**\n\n"
            "Could not find a valid Google API key in `.env` or system environment. "
            "Please ensure `GOOGLE_API_KEY` is configured in `.env`."
        )

    prompt = f"""You are an experienced GCSE {subject} examiner and teacher providing model answers.

A student needs an examiner-standard walkthrough for the following exam question worth {marks} mark(s):

\"\"\"{question}\"\"\"

Please provide your answer with the following clear markdown headings:

## 📝 Step-by-Step Solution
Provide clear, numbered step-by-step working showing exactly how to answer this question.
For any Maths equations, fractions, or algebraic working, ALWAYS use standard LaTeX enclosed in $ or $$.

## 🎯 Mark Breakdown
Explain specifically where each of the {marks} marks is awarded according to standard GCSE mark scheme criteria. Format as a bullet list.

## 💡 Examiner Tips & Common Pitfalls
Give 1-2 actionable tips on common mistakes students make on this type of question.

Keep the response concise, exam-focused, and encouraging. Use markdown formatting."""

    # Build parts list
    parts: List[dict] = []
    
    # Add image if provided
    if image_file is not None:
        try:
            image_bytes = image_file.getvalue() if hasattr(image_file, "getvalue") else image_file.read()
            mime_type = getattr(image_file, "type", "image/jpeg") or "image/jpeg"
            b64_img = base64.b64encode(image_bytes).decode("utf-8")
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": b64_img
                }
            })
        except Exception as e:
            return f"⚠️ **Error Reading Uploaded Image**: {e}"

    parts.append({"text": prompt})
    request_body = json.dumps({"contents": [{"parts": parts}]}).encode("utf-8")

    last_error = ""
    # Try candidate models with fallback
    for model_name in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=request_body,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts_out = candidates[0].get("content", {}).get("parts", [])
                    if parts_out:
                        return parts_out[0].get("text", "No text returned.")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
                err_msg = err_json.get("error", {}).get("message", err_body)
            except Exception:
                err_msg = err_body
            last_error = f"HTTP {e.code} ({model_name}): {err_msg}"
            time.sleep(1.0)
            continue
        except Exception as e:
            last_error = f"{type(e).__name__} ({model_name}): {e}"
            time.sleep(0.5)
            continue

    return (
        f"⚠️ **AI Tutor Service Notice**\n\n"
        f"Unable to generate response. Details:\n\n`{last_error}`\n\n"
        f"*Tip: If you recently exceeded the free tier rate limit (5 requests/min), please wait a few seconds and try again.*"
    )

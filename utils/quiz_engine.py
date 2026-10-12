import random
import copy


def generate_quiz(quiz_bank: list[dict], n: int = 10) -> list[dict]:
    """Randomly sample n questions from the bank. Each call gives a different set."""
    pool = copy.deepcopy(quiz_bank)
    random.shuffle(pool)
    return pool[:min(n, len(pool))]


def evaluate_quiz(questions: list[dict], answers: dict[int, int]) -> dict:
    """
    Evaluate submitted answers.
    answers: {question_index: selected_option_index}
    Returns dict with score, pct, and per-question breakdown.
    """
    total = len(questions)
    correct = 0
    breakdown = []
    for i, q in enumerate(questions):
        selected = answers.get(i, -1)
        ans_idx = q.get("answer_index", q.get("correct_answer", 0))
        is_correct = (selected == ans_idx)
        if is_correct:
            correct += 1
        breakdown.append({
            "question": q["question"],
            "options": q["options"],
            "selected": selected,
            "answer_index": ans_idx,
            "correct": is_correct,
            "explanation": q.get("explanation", ""),
        })
    pct = round(correct / total * 100) if total else 0
    return {"score": correct, "total": total, "pct": pct, "breakdown": breakdown}

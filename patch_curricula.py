import os
import json
import random

DIR = "curriculum_data"
categories = ["Algebra", "Geometry", "Number", "Statistics", "Probability", "Cell Biology", "Organisation", "Infection", "Bioenergetics", "Ecology"]

for fname in os.listdir(DIR):
    if not fname.endswith(".json"): continue
    path = os.path.join(DIR, fname)
    with open(path, "r") as f:
        data = json.load(f)
    
    for topic in data.get("topics", []):
        if "category" not in topic:
            # Assign dummy category if none
            topic["category"] = random.choice(categories)
        
        # Generate 15 dummy quiz questions for the bank
        if "quiz_bank" not in topic:
            quiz_bank = []
            for i in range(15):
                quiz_bank.append({
                    "question": f"Sample knowledge check question {i+1} for {topic['title']}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer_index": random.randint(0, 3),
                    "explanation": "This is the correct answer because of the core concepts taught in the lesson."
                })
            topic["quiz_bank"] = quiz_bank

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

print("Patched all JSON curricula.")

import os
import json

DIR = "curriculum_data"
for fname in os.listdir(DIR):
    if not fname.endswith(".json"): continue
    path = os.path.join(DIR, fname)
    with open(path, "r") as f:
        data = json.load(f)
    
    for t in data.get("topics", []):
        t["detailed_slides"] = [
            f"### Slide 1: Introduction to {t['title']}\n\n- The core concepts for this topic are essential for your exam.\n- Ensure you understand the underlying principles before attempting past papers.\n- Review your textbook notes to supplement this slide.",
            "### Slide 2: Key Formulas & Rules\n\n- Always write down the formula before substituting numbers.\n- Pay close attention to units in your final answer.\n- Show every step of your working to guarantee method marks.",
            "### Slide 3: Common Mistakes\n\n- Watch out for sign errors (e.g. subtracting a negative).\n- Always double-check your calculations at the end.\n- Don't rush through the final steps of a multi-part question."
        ]
        
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

print("Fast patch complete.")

import json
import time
import os
import google.generativeai as genai

# Manually parse .env to avoid missing dotenv dependency
api_key = None
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("GOOGLE_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                break

if api_key:
    genai.configure(api_key=api_key)
else:
    print("Could not find GOOGLE_API_KEY in .env")
    exit(1)

MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]

def get_more_questions(topic_title, subject, existing_count):
    prompt = f"""You are an expert GCSE {subject} teacher.
We already have {existing_count} questions for the topic "{topic_title}".
We need to expand our quiz bank with 10 BRAND NEW, UNIQUE, and HIGHLY CHALLENGING multiple-choice questions for this topic. Do not repeat standard basic questions.

Provide your response strictly as a JSON object with one key: "quiz_bank".
- "quiz_bank": An array of exactly 10 objects representing multiple choice questions. Each object must have:
  "question": string
  "options": array of exactly 4 string options
  "answer_index": integer (0 to 3) representing the correct option
  "explanation": string (why this is correct)

CRITICAL FORMATTING INSTRUCTION: 
For any mathematical formulas, numbers, fractions, or equations, you MUST use standard LaTeX math mode enclosed in $ or $$. 
- Do NOT use basic text for fractions like "a/b" or "1 3/5". ALWAYS use $\\frac{{a}}{{b}}$ or $1\\frac{{3}}{{5}}$.
- Do NOT use "*" for multiplication. ALWAYS use $\\times$.
- Do NOT use "^" without enclosing in math mode. Use $x^2$.
"""
    for model_name in MODELS:
        try:
            m = genai.GenerativeModel(model_name)
            response = m.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text.strip()).get("quiz_bank", [])
        except Exception as e:
            err = str(e)
            if "429" in err or "Quota" in err or "ResourceExhausted" in err:
                print(f"Rate limited or quota exceeded on {model_name}. Trying next model...")
                continue
            else:
                time.sleep(3)
    return []

print("Starting Phase 1: Finishing off Biology")
os.system("python3 enrich_curriculum.py")

print("\nStarting Phase 2: Expanding Maths Quiz Banks")
with open("curriculum_data/maths.json", "r") as f:
    data = json.load(f)

# Iterate and expand
for i, t in enumerate(data.get("topics", [])):
    existing_len = len(t.get("quiz_bank", []))
    if existing_len >= 25:
        print(f"  [{i+1}/{len(data['topics'])}] Skipping {t['title']}, already has {existing_len} questions.")
        continue
        
    print(f"  [{i+1}/{len(data['topics'])}] Generating +10 extra questions for: {t['title']}")
    new_qs = get_more_questions(t["title"], "Mathematics", existing_len)
    
    if new_qs:
        t["quiz_bank"].extend(new_qs)
        print(f"    -> Successfully added {len(new_qs)} questions. Total is now {len(t['quiz_bank'])}.")
        
        with open("curriculum_data/maths.json", "w") as f:
            json.dump(data, f, indent=2)
            
    time.sleep(4.1)

print("Daily generation complete.")

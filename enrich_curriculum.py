import os
import json
import time
import sys
import google.generativeai as genai

# Load API key robustly
api_key = None
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read()
        if 'GOOGLE_API_KEY=' in content:
            api_key = content.split('GOOGLE_API_KEY=')[1].split('\n')[0].strip()

if api_key:
    genai.configure(api_key=api_key)
else:
    print("Could not find GOOGLE_API_KEY in .env")
    exit(1)

def generate_content(topic_title, subject):
    prompt = f"""You are an expert GCSE {subject} teacher.
We need curriculum content for the topic: "{topic_title}".

Provide your response strictly as a JSON object with two keys: "detailed_slides" and "quiz_bank".

Format requirements:
- "detailed_slides": An array of exactly 4 strings. Each string is a detailed markdown slide (start with an h3 title like ### Slide 1: [Title]).
- "quiz_bank": An array of exactly 15 objects representing multiple choice questions. Each object must have:
  "question": string
  "options": array of exactly 4 string options
  "answer_index": integer (0 to 3) representing the correct option
  "explanation": string (why this is correct)

Make the questions extremely relevant to {topic_title} at the GCSE level.
"""
    if "Biology" in subject:
        prompt += """
CRITICAL BIOLOGY INSTRUCTIONS:
1. LEVEL: The content MUST be strictly at the **AQA GCSE Biology** level. Do NOT include any A-Level concepts, terminology, or depth. Keep it strictly within the bounds of a GCSE specification.
2. SLIDES: Make your slides detailed for a GCSE student, wrapping all **key GCSE biological terms in bold**. 
3. QUESTIONS: Design the 15 multiple-choice questions to mimic "5 or 6 mark" AQA GCSE exam questions (e.g., evaluating an experiment, reading data, applied scenarios). Ensure the distractors are common GCSE misconceptions, not A-level facts.
"""
    else:
        prompt += """
CRITICAL FORMATTING INSTRUCTION: 
For any mathematical formulas, numbers, fractions, or equations, you MUST use standard LaTeX math mode enclosed in $ or $$. 
- Do NOT use basic text for fractions like "a/b" or "1 3/5". ALWAYS use $\frac{{a}}{{b}}$ or $1\frac{{3}}{{5}}$.
- Do NOT use "*" for multiplication. ALWAYS use $\times$.
- Do NOT use "^" without enclosing in math mode. Use $x^2$.
"""
    models_to_try = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]
    for model_name in models_to_try:
        try:
            m = genai.GenerativeModel(model_name)
            response = m.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.strip()
            return json.loads(text)
        except Exception as e:
            err = str(e)
            if "429" in err or "ResourceExhausted" in err or "Quota" in err:
                print(f"Rate limited or quota exceeded on {model_name}. Trying next model...", flush=True)
                continue
            else:
                print(f"Error on {model_name}: {err[:80]}. Retrying...", flush=True)
                time.sleep(3)
    return None

DIR = "curriculum_data"
for fname in os.listdir(DIR):
    if not fname.endswith(".json"): continue
    path = os.path.join(DIR, fname)
    with open(path, "r") as f:
        data = json.load(f)
    
    subject = data.get("subject", "GCSE Subject")
    print(f"Processing {subject}...", flush=True)
    
    modified = False
    for i, t in enumerate(data.get("topics", [])):
        if t["id"] == "math_algebra_quadratics":
            continue
            
        is_mock = False
        if t.get("quiz_bank"):
            first_q = t["quiz_bank"][0].get("question", "")
            if "relating to" in first_q or "Mock Data" in first_q:
                is_mock = True
                
        if len(t.get("quiz_bank", [])) >= 15 and not is_mock:
            print(f"  [{i+1}/{len(data['topics'])}] Skipping already enriched topic: {t['title']}", flush=True)
            continue
            
        print(f"  [{i+1}/{len(data['topics'])}] Generating content for: {t['title']}", flush=True)
        result = generate_content(t["title"], subject)
        if result:
            t["detailed_slides"] = result.get("detailed_slides", [])
            t["quiz_bank"] = result.get("quiz_bank", [])
            modified = True
            
        time.sleep(4.1) # strictly respect 15 RPM free tier limit
        
        # Save incrementally
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

print("Enrichment completely finished.", flush=True)

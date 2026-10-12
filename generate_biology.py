import os
import json
import time
import sys
import google.generativeai as genai

# Load API key from .env
api_key = None
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('GOOGLE_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
                break

if not api_key:
    print("Could not find GOOGLE_API_KEY in .env")
    sys.exit(1)

genai.configure(api_key=api_key)

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest"
]

current_model_idx = 0

def get_current_model():
    global current_model_idx
    if current_model_idx >= len(MODELS):
        return None, None
    name = MODELS[current_model_idx]
    return name, genai.GenerativeModel(name)

def generate_topic_content(topic_title):
    global current_model_idx
    prompt = f"""You are an expert GCSE Biology teacher specializing in the AQA exam board.
We need curriculum content for the topic: "{topic_title}".

Provide your response strictly as a JSON object with two keys: "detailed_slides" and "quiz_bank".

Format requirements:
- "detailed_slides": An array of exactly 4 strings. Each string is a comprehensive markdown slide (start with an h3 title like ### Slide 1: [Title]).
  * CRITICAL: Keep content strictly within the AQA GCSE Biology syllabus. Absolutely no A-Level content or advanced biochemical terms.
  * Wrap all key GCSE biological terms in **bold**.
  * Include clear explanations, bullet points, and examiner tips for common student pitfalls.

- "quiz_bank": An array of exactly 15 objects representing multiple-choice questions. Each object must have:
  "question": string (scenario-based, application, or 5/6 mark style questions like required practicals, interpreting experimental data, evaluating hypotheses)
  "options": array of exactly 4 string options
  "answer_index": integer (0 to 3) representing the correct option
  "explanation": string (detailed explanation of why the answer is correct and why common misconceptions are wrong)

All distractors must be realistic GCSE-level misconceptions.
"""
    while current_model_idx < len(MODELS):
        model_name, model = get_current_model()
        if not model:
            print("All models exhausted.")
            return None

        print(f"    [Using {model_name}] Requesting content for: {topic_title}...", flush=True)
        try:
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.strip()
            data = json.loads(text)
            
            slides = data.get("detailed_slides", [])
            quiz = data.get("quiz_bank", [])
            
            if len(slides) >= 4 and len(quiz) >= 10:
                return data
            else:
                print(f"    Received incomplete data ({len(slides)} slides, {len(quiz)} questions). Retrying...", flush=True)
                time.sleep(2)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg or "Quota" in err_msg:
                if "free_tier_requests" in err_msg or "per day" in err_msg.lower() or "quota exceeded" in err_msg.lower():
                    print(f"    Daily quota reached on {model_name}. Switching to next model...", flush=True)
                    current_model_idx += 1
                else:
                    print(f"    Per-minute rate limit hit on {model_name}. Sleeping 10s...", flush=True)
                    time.sleep(10)
            else:
                print(f"    Error with {model_name}: {err_msg[:120]}. Retrying...", flush=True)
                time.sleep(5)
                
    return None

def main():
    bio_path = "curriculum_data/biology.json"
    with open(bio_path, "r") as f:
        curriculum = json.load(f)

    topics = curriculum.get("topics", [])
    total_topics = len(topics)
    print(f"=== Starting Biology Enrichment ({total_topics} topics total) ===", flush=True)

    completed_count = 0
    for idx, t in enumerate(topics, 1):
        has_slides = len(t.get("detailed_slides", [])) >= 4
        has_quiz = len(t.get("quiz_bank", [])) >= 10
        
        if has_slides and has_quiz:
            print(f"[{idx}/{total_topics}] Already complete: {t['title']} ({len(t['detailed_slides'])} slides, {len(t['quiz_bank'])} questions)", flush=True)
            completed_count += 1
            continue

        print(f"[{idx}/{total_topics}] Generating AQA GCSE Biology content for: {t['title']}...", flush=True)
        result = generate_topic_content(t["title"])
        
        if result:
            t["detailed_slides"] = result.get("detailed_slides", [])
            t["quiz_bank"] = result.get("quiz_bank", [])
            completed_count += 1
            print(f"  ✓ Successfully saved: {t['title']} ({len(t['detailed_slides'])} slides, {len(t['quiz_bank'])} questions)", flush=True)
            
            # Save immediately after each topic
            with open(bio_path, "w") as f:
                json.dump(curriculum, f, indent=2)
        else:
            print(f"  ✗ Failed to generate content for: {t['title']}", flush=True)

        # 4.5 second delay to strictly respect 15 RPM
        time.sleep(4.5)

    print(f"\n=== Enrichment Finished: {completed_count}/{total_topics} Biology topics completed! ===", flush=True)

if __name__ == "__main__":
    main()

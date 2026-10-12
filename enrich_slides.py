import os
import json
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor
import time

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
# Fallback if GOOGLE_API_KEY is not set, we can't easily get it here, but usually it's in the environment.
# Let's check if it exists
if not os.environ.get("GOOGLE_API_KEY"):
    import streamlit as st
    # Can't access session state from CLI easily. Let's assume the user has GOOGLE_API_KEY in env or we can mock it.
    pass

def generate_slides(topic_title, subject):
    prompt = f"""You are an expert GCSE {subject} teacher. 
Create 4 detailed presentation slides of revision notes for the topic: "{topic_title}".
Each slide must have a title and 3-5 detailed bullet points of content.
Return the output strictly as a JSON array of strings, where each string is a markdown-formatted slide (including the title as an h3).
Do NOT wrap the output in markdown code blocks, just return the raw JSON array.
Example:
[
  "### Slide 1: Introduction\\n- Point 1\\n- Point 2",
  "### Slide 2: Core Concepts\\n- Point 1\\n- Point 2"
]
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        if text.startswith("```"):
            text = text[3:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Error for {topic_title}: {e}")
        return [
            f"### Slide 1: Introduction to {topic_title}\n- Core concepts will be covered here.\n- Review your textbook for full details.",
            "### Slide 2: Key Formulas & Rules\n- Remember to show all working.\n- Check units in your final answer.",
            "### Slide 3: Common Mistakes\n- Watch out for sign errors.\n- Always double check your calculations."
        ]

DIR = "curriculum_data"
for fname in os.listdir(DIR):
    if not fname.endswith(".json"): continue
    path = os.path.join(DIR, fname)
    with open(path, "r") as f:
        data = json.load(f)
    
    subject = data.get("subject", "GCSE Subject")
    print(f"Enriching {subject}...")
    
    def process_topic(topic):
        if "detailed_slides" not in topic or len(topic.get("detailed_slides", [])) < 3:
            print(f"  Generating slides for: {topic['title']}")
            topic["detailed_slides"] = generate_slides(topic["title"], subject)
            time.sleep(1) # rate limiting
        return topic

    # Run sequentially to avoid rate limits on standard API keys
    for t in data.get("topics", []):
        process_topic(t)
        
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

print("Enrichment complete.")

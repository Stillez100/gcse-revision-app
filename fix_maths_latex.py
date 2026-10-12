import json
import re

def process_text(text):
    if not isinstance(text, str): return text
    
    # Replace instances like "1 3/5" with "$1\frac{3}{5}$"
    text = re.sub(r'(?<!\$)\b(\d+)\s+(\d+)/(\d+)\b(?!\$)', r'$\1\\frac{\2}{\3}$', text)
    
    # Replace instances like "2/3" with "$\frac{2}{3}$"
    text = re.sub(r'(?<!\$)(?<!\d/)(\d+)/(\d+)(?!/\d)(?!\$)', r'$\\frac{\1}{\2}$', text)
    
    # Replace " * " with " \times " 
    text = text.replace(" * ", " $\\times$ ")
    
    # Replace "^2" or "^3" etc with standard math wrapping
    text = re.sub(r'(?<!\$)\b([a-zA-Z0-9]+)\^(\d+)\b(?!\$)', r'$\1^\2$', text)
    
    return text

def process_item(item):
    if isinstance(item, dict):
        for k, v in item.items():
            if k in ["question", "explanation"]:
                item[k] = process_text(v)
            elif k == "options" and isinstance(v, list):
                item[k] = [process_text(opt) for opt in v]
            elif k == "detailed_slides" and isinstance(v, list):
                item[k] = [process_text(s) for s in v]
            elif isinstance(v, (dict, list)):
                process_item(v)
    elif isinstance(item, list):
        for i in item:
            process_item(i)

with open('curriculum_data/maths.json', 'r') as f:
    data = json.load(f)

for topic in data.get('topics', []):
    process_item(topic)

with open('curriculum_data/maths.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Maths formatting updated successfully!")

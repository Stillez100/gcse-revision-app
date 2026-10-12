import re

with open("app.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Fix the `lesson_tabs = st.tabs...` indentation to be 20 spaces instead of 16
    if "lesson_tabs = st.tabs" in line:
        lines[i] = "                    lesson_tabs = st.tabs([\"📚 Notes & Slides\", \"✅ Knowledge Check\"])\n"
    # Fix the `categories = {}` indentation to be 12 spaces instead of 12? wait
    # line 167: '            with subj_tabs[0]:' -> should be 8 spaces
    if "with subj_tabs[0]:" in line and not line.startswith("        with"):
        lines[i] = "        with subj_tabs[0]:\n"
    # line 169: '            categories = {}'
    if "categories = {}" in line and not line.startswith("            categories"):
        lines[i] = "            categories = {}\n"

with open("app.py", "w") as f:
    f.writelines(lines)

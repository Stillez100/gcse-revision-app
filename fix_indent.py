with open("app.py", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "with subj_tabs[0]:" in lines[i]:
        lines[i] = "        with subj_tabs[0]:\n"
    elif "categories = {}" in lines[i]:
        lines[i] = "            categories = {}\n"

with open("app.py", "w") as f:
    f.writelines(lines)

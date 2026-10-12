import sys

with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Change the lesson tabs
    if "lesson_tabs = st.tabs([\"📚 Notes & Slides\", \"✅ Knowledge Check\", \"🤖 AI Exam Helper\"])" in line:
        new_lines.append(line.replace(" \"🤖 AI Exam Helper\"", ""))
        continue
        
    # Inject the subject tabs
    if line.strip() == "st.markdown(\"---\")" and i > 150 and i < 170:
        new_lines.append(line)
        new_lines.append("        subj_tabs = st.tabs([\"📚 Curriculum & Lessons\", \"🤖 Ask AI Tutor\"])\n")
        new_lines.append("        with subj_tabs[0]:\n")
        continue

    # Skip the old AI Exam helper block completely
    if line.strip() == "# AI Exam Helper":
        # We need to skip until the end of the file or next major block
        pass
        
    new_lines.append(line)

# Now we need to indent lines between `with subj_tabs[0]:` and `# AI Exam Helper`
with open("app.py", "r") as f:
    content = f.read()

# Let's do it with regex or targeted string replacements instead.
import re

# 1. Replace the st.markdown("---") at subject level with the tab creation
content = content.replace(
    '        st.markdown("---")\n        \n        # Group topics by Category',
    '        st.markdown("---")\n        subj_tabs = st.tabs(["📚 Curriculum & Lessons", "🤖 Ask AI Tutor"])\n        with subj_tabs[0]:\n            # Group topics by Category'
)

# 2. Indent everything from '# Group topics by Category' down to '# AI Exam Helper'
# Actually, a simpler way is to just use standard python replacement.
lines = content.split('\n')
inside_subj_tab = False
inside_ai_helper = False
final_lines = []

for line in lines:
    if 'subj_tabs = st.tabs(["📚 Curriculum & Lessons"' in line:
        final_lines.append(line)
        inside_subj_tab = True
        continue
        
    if 'lesson_tabs = st.tabs(["📚 Notes & Slides", "✅ Knowledge Check"' in line:
        final_lines.append(line.replace(', "🤖 AI Exam Helper"', ''))
        continue

    if '# AI Exam Helper' in line:
        inside_ai_helper = True
        
    if inside_subj_tab and not inside_ai_helper and line.startswith('        '):
        if line.strip() != '' and not line.startswith('        subj_tabs'):
            # Indent by 4 spaces if it belongs to the loop
            final_lines.append('    ' + line)
        else:
            final_lines.append(line)
    elif not inside_ai_helper:
        final_lines.append(line)

# Add the new AI tutor at the end of the subject loop
ai_tutor_code = """
        with subj_tabs[1]:
            st.markdown("### 🤖 Subject AI Tutor")
            st.write(f"Stuck on a specific {subject_name} concept or a past paper question? Ask me below!")
            
            user_q = st.text_area("What do you need help with?", key=f"ai_q_subj_{subject_name}")
            
            st.markdown("**Optional: Attach an image of the question**")
            user_img = st.file_uploader("Upload Image (PNG/JPG)", type=["png", "jpg", "jpeg"], key=f"ai_img_subj_{subject_name}")
            
            user_marks = st.number_input("Number of Marks (if applicable):", min_value=1, max_value=10, value=3, key=f"ai_marks_subj_{subject_name}")
            
            if st.button("Generate Solution", key=f"ai_btn_subj_{subject_name}"):
                if user_q.strip() or user_img:
                    with st.spinner("Generating expert solution..."):
                        from utils.ai_tutorial import generate_solution
                        solution = generate_solution(user_q, user_marks, subject_name, image_file=user_img)
                        st.markdown(solution)
                else:
                    st.warning("Please enter a question or upload an image first.")
"""

final_lines.extend(ai_tutor_code.split('\n'))

with open("app.py", "w") as f:
    f.write('\n'.join(final_lines))

print("Patched app.py")

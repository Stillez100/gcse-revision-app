# 🎓 GCSE Revision Web Application

A full-featured GCSE revision web application built with **Python**, **Streamlit**, and **Streamlit Authenticator**. It includes multi-subject selector tabs, exam tutorial layouts, model worked answers, practice past-paper style questions, and session progress tracking.

---

## 📁 Project Structure

```text
gcse_revision_app/
├── app.py                      # Main Streamlit application entry point
├── config.yaml                 # Streamlit Authenticator configuration & credentials
├── requirements.txt            # Python dependencies
├── generate_keys.py            # Password hashing script for config.yaml
├── README.md                   # Documentation and quickstart guide
├── curriculum_data/            # Subject specification & tutorial data
│   ├── maths.json              # GCSE Mathematics (Quadratics, Pythagoras, etc.)
│   ├── biology.json            # GCSE Biology (Mitosis, Cell cycle, etc.)
│   ├── chemistry.json          # GCSE Chemistry (Ionic bonding, Lattices, etc.)
│   ├── physics.json            # GCSE Physics (Energy conservation, etc.)
│   └── english_literature.json # GCSE English Literature (Macbeth, themes, etc.)
├── utils/
│   ├── __init__.py
│   ├── auth_helper.py          # Authentication handling with fallback resilience
│   └── data_loader.py          # Curriculum loading and user progress tracking
└── assets/
    └── style.css               # GCSE exam portal modern design system
```

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```

---

## 🔐 Demo Credentials

The application is pre-configured with two user accounts:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Student (Candidate)** | `student` | `student123` | Target Grade 8, candidate progress tracking |
| **Teacher (Tutor)** | `teacher` | `teacher123` | Head of Revision role |

*(To generate new hashed credentials for `config.yaml`, run `python generate_keys.py`)*

---

## ✨ Features Included

1. **Authentication**:
   - `streamlit-authenticator` cookie-based login with fallback support.
   - User profile bar, target grade indicator, and logout button.

2. **Multi-Subject Selector Tabs**:
   - Tabs for **Mathematics 📐**, **Biology 🧬**, **Chemistry 🧪**, **Physics ⚡**, and **English Literature 📖**.
   - Exam board selector (**AQA**, **Edexcel**, **OCR**).
   - Tier filter (**Higher**, **Foundation**, or **All**).

3. **Exam Tutorial Layout**:
   - **Specification Objectives**: Checklist of exam board learning criteria.
   - **Core Concepts & Theory**: Key definitions, LaTeX formulas, and golden exam rules.
   - **Worked Model Answers**: Step-by-step examiner walkthroughs with examiner tips and common pitfalls.
   - **Interactive Practice Exam Questions**: Past-paper style questions, hint triggers, student answer box, official mark scheme reveal, and self-marking slider.
   - **Progress Tracker**: Sidebar metrics showing completion percentage, accuracy rate, and mastery status per topic.

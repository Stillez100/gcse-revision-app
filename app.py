import os
from datetime import datetime
import streamlit as st
from utils.auth_helper import get_authenticator, render_login_page, render_user_header
from utils.data_loader import (
    load_all_curricula,
    init_user_progress,
    get_topic_progress,
    update_topic_quiz_score,
    calculate_overall_stats,
    calculate_subject_stats,
    get_recent_subject_attempts,
    get_ragp_color
)
from utils.quiz_engine import generate_quiz, evaluate_quiz
from utils.ai_tutorial import generate_solution
from utils.category_images import get_category_svg

RAGP_HEX_MAP = {
    "Pink": "#F43F5E",
    "Green": "#22C55E",
    "Amber": "#F59E0B",
    "Red": "#EF4444",
    "None": "#94A3B8"
}

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="GCSE Exam Master | Revision Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS Loader
# ---------------------------------------------------------
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
init_user_progress()

# ---------------------------------------------------------
# Authentication Gate
# ---------------------------------------------------------
authenticator, has_stauth = get_authenticator()
auth_status = render_login_page(authenticator=authenticator, has_stauth=has_stauth)

if not auth_status:
    st.stop()

curricula = load_all_curricula()
overall_stats = calculate_overall_stats(curricula)

if not curricula:
    st.warning("⚠️ No curriculum data found in `curriculum_data/`. Please ensure JSON files are present.")
    st.stop()

# ---------------------------------------------------------
# Navigation & Layout
# ---------------------------------------------------------
render_user_header(authenticator=authenticator)

if st.session_state.get("page") == "profile":
    st.markdown("## ⚙️ Profile Settings")
    st.markdown("Update your personal details below.")
    
    new_name = st.text_input("First Name", value=st.session_state.get("name", ""))
    
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        
    username = st.session_state.get("username")
    saved_target = "8"
    if username and username in config["credentials"]["usernames"]:
        saved_target = config["credentials"]["usernames"][username].get("target_grade", "8")
        
    target_grade_opts = ["9", "8", "7", "6", "5", "4", "3", "2", "1"]
    current_grade = st.session_state.get("target_grade", saved_target)
    if current_grade not in target_grade_opts: current_grade = "8"
    new_target = st.selectbox("Target Grade", options=target_grade_opts, index=target_grade_opts.index(current_grade))
    
    if st.button("Save Changes", type="primary"):
        st.session_state["name"] = new_name
        st.session_state["target_grade"] = new_target
        
        import yaml
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        username = st.session_state.get("username")
        if username and username in config["credentials"]["usernames"]:
            config["credentials"]["usernames"][username]["name"] = new_name
            config["credentials"]["usernames"][username]["target_grade"] = new_target
            
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)
            
        st.success("Profile updated successfully! Your sidebar profile has been refreshed.")
        st.rerun()
        
    if st.button("⬅️ Back to Dashboard"):
        st.session_state["page"] = "home"
        st.rerun()
    
    st.stop()

subject_names = list(curricula.keys())
tab_titles = ["🏠 Home"] + [f"{curricula[name].get('icon', '📚')} {name}" for name in subject_names]

st.sidebar.markdown("### 🧭 Navigation")
page_selection = st.sidebar.radio("Nav", tab_titles, label_visibility="collapsed", key="main_nav_radio")

# ---------------------------------------------------------
# RAG TOOLTIPS HELPER
# ---------------------------------------------------------
def make_rag_tooltip_html(color, count=None, score=None, label_override=None, align="center"):
    """
    Renders an accessible RAG badge with interactive hover tooltip popup
    explaining exactly what the status/score represents in AQA GCSE revision.
    """
    align_class = f"align-{align}" if align != "center" else ""
    c_lower = (color or "none").lower()
    if c_lower not in ["green", "amber", "red", "pink", "none"]:
        c_lower = "none"

    if c_lower == "green":
        status_name = "🟢 Mastered (Score 70–99%)"
        rule = "Criteria: 70% – 99% Score"
        meaning = "Secure subject knowledge & exam readiness. Key definitions, formulas, and application skills verified."
        default_label = f"🟢 {count}" if count is not None else (f"🟢 {score}% • Mastered" if score is not None else "🟢 Mastered")
    elif c_lower == "amber":
        status_name = "🟡 Revising (Score 50–69%)"
        rule = "Criteria: 50% – 69% Score"
        meaning = "Solid foundational grasp. Targeted exam practice needed to push into higher GCSE grade boundaries."
        default_label = f"🟡 {count}" if count is not None else (f"🟡 {score}% • Revising" if score is not None else "🟡 Revising")
    elif c_lower == "pink":
        status_name = "🌸 Perfect Mastery (Score 100%)"
        rule = "Criteria: 10/10 Correct (100% Score)"
        meaning = "Flawless exam performance! Full marks achieved with complete accuracy."
        default_label = f"🌸 {count}" if count is not None else (f"🌸 {score}% • Perfect" if score is not None else "🌸 100%")
    elif c_lower == "red":
        status_name = "🔴 Priority Focus (Score <50%)"
        rule = "Criteria: Score Below 50%"
        meaning = "High-priority revision area. Concept gaps identified — review slides and retake the 10-question check."
        default_label = f"🔴 {count}" if count is not None else (f"🔴 {score}% • Focus" if score is not None else "🔴 Priority")
    else:  # none / unattempted
        status_name = "⚪ Unattempted"
        rule = "Criteria: Quiz Pending"
        meaning = "10 diagnostic exam questions ready. Complete the knowledge check to establish your RAG baseline."
        default_label = f"⚪ {count}" if count is not None else "⚪ Not Started"

    badge_label = label_override if label_override else default_label
    tooltip_title = status_name
    if count is not None and not label_override:
        tooltip_title += f" • {count} Lesson{'s' if count != 1 else ''}"
    elif score is not None and not label_override:
        tooltip_title += f" • Score: {score}%"

    native_title = f"{tooltip_title} | {rule}: {meaning}"

    return (
        f'<div class="rag-tooltip-wrap {align_class}" title="{native_title}">'
        f'<span class="rag-pill {c_lower}">{badge_label}</span>'
        f'<div class="rag-popup">'
        f'<div class="rag-popup-badge {c_lower}">{tooltip_title}</div>'
        f'<div class="rag-popup-rule">{rule}</div>'
        f'<div class="rag-popup-meaning">{meaning}</div>'
        f'</div>'
        f'</div>'
    )

# ---------------------------------------------------------
# HOME TAB
# ---------------------------------------------------------
if page_selection == tab_titles[0]:
    st.markdown("""
    <div class="main-header" style="margin-bottom: 1.25rem;">
        <h1 style="color: #F8FAFC; font-size: 1.85rem; font-weight: 800; margin-bottom: 0.2rem; display: flex; align-items: center; gap: 0.5rem;">
            <span>🎓</span>
            <span>GCSE Revision Command Centre</span>
        </h1>
        <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">Comprehensive specification breakdowns, diagnostic progress tracking, and instant exam practice.</p>
    </div>
    """, unsafe_allow_html=True)
    
    left_col, right_col = st.columns([1, 1], gap="large")
    
    # ── Left Column: Overall Progress Summary ─────────────────────
    with left_col:
        st.markdown("""
        <div class="home-dashboard-card">
            <div class="home-card-header">
                <span class="home-card-header-title">📊 Overall Revision Progress</span>
                <span class="home-badge-pill">All GCSE Subjects</span>
            </div>
        """, unsafe_allow_html=True)
        
        overall_pct = overall_stats.get("completion_pct", 0)
        st.progress(overall_pct / 100.0)
        
        overall_avg = overall_stats.get("avg_score")
        if overall_avg is not None:
            avg_color = get_ragp_color(overall_avg)
            avg_color_hex = RAGP_HEX_MAP.get(avg_color, "#94A3B8")
            avg_badge_html = f'<span class="cat-score-badge" style="background: {avg_color_hex}18; color: {avg_color_hex}; border: 1px solid {avg_color_hex}45; font-size: 0.8rem; padding: 0.15rem 0.55rem;">{overall_avg}% • {avg_color}</span>'
        else:
            avg_badge_html = '<span class="cat-score-badge" style="background: #162032; color: #94A3B8; border: 1px solid #334155; font-size: 0.8rem; padding: 0.15rem 0.55rem;">Not Started</span>'
            
        overview_html = (
            f'<div class="home-stat-overview-box">'
            f'<div class="home-stat-row">'
            f'<span><b>Lessons Completed:</b></span>'
            f'<span style="font-weight: 800; color: #F8FAFC;">{overall_stats["completed"]} / {overall_stats["total_topics"]} ({overall_pct}%)</span>'
            f'</div>'
            f'<div class="home-stat-row" style="margin-bottom: 0;">'
            f'<span><b>Average Score Across Subjects:</b></span>'
            f'<span>{avg_badge_html}</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(overview_html, unsafe_allow_html=True)
        
        kpi_grid_html = (
            f'<div class="home-kpi-grid">'
            f'<div class="home-kpi-box" style="border-left: 4px solid #F43F5E;">'
            f'<span class="home-kpi-label">🌸 Perfect Mastery</span>'
            f'<span class="home-kpi-val" style="color: #FB7185;">{overall_stats["Pink"]} <span style="font-size: 0.75rem; font-weight: 600; color: #94A3B8;">lessons</span></span>'
            f'</div>'
            f'<div class="home-kpi-box" style="border-left: 4px solid #22C55E;">'
            f'<span class="home-kpi-label">🟢 Mastered (≥70%)</span>'
            f'<span class="home-kpi-val" style="color: #4ADE80;">{overall_stats["Green"]} <span style="font-size: 0.75rem; font-weight: 600; color: #94A3B8;">lessons</span></span>'
            f'</div>'
            f'<div class="home-kpi-box" style="border-left: 4px solid #F59E0B;">'
            f'<span class="home-kpi-label">🟡 Revising (50–69%)</span>'
            f'<span class="home-kpi-val" style="color: #FBBF24;">{overall_stats["Amber"]} <span style="font-size: 0.75rem; font-weight: 600; color: #94A3B8;">lessons</span></span>'
            f'</div>'
            f'<div class="home-kpi-box" style="border-left: 4px solid #EF4444;">'
            f'<span class="home-kpi-label">🔴 Priority Focus (<50%)</span>'
            f'<span class="home-kpi-val" style="color: #F87171;">{overall_stats["Red"]} <span style="font-size: 0.75rem; font-weight: 600; color: #94A3B8;">lessons</span></span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(kpi_grid_html, unsafe_allow_html=True)
        
        tooltips_strip = (
            f'<div style="font-size: 0.74rem; font-weight: 700; color: #64748B; margin-bottom: 0.4rem;">Hover RAGP Reference:</div>'
            f'<div class="cat-rag-summary" style="margin-bottom: 0.4rem;">'
            f'{make_rag_tooltip_html("Pink", count=overall_stats["Pink"])}'
            f'{make_rag_tooltip_html("Green", count=overall_stats["Green"])}'
            f'{make_rag_tooltip_html("Amber", count=overall_stats["Amber"])}'
            f'{make_rag_tooltip_html("Red", count=overall_stats["Red"])}'
            f'{make_rag_tooltip_html("None", count=overall_stats.get("None", 0))}'
            f'</div>'
        )
        st.markdown(tooltips_strip, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Right Column: Subject Focus, Recent Attempts & Study Link ─
    with right_col:
        sorted_subjects = sorted(list(curricula.keys()))
        
        st.markdown("""
        <div class="home-dashboard-card">
            <div class="home-card-header">
                <span class="home-card-header-title">🎯 Subject Focus & Performance</span>
                <span class="home-badge-pill">Subject Drilldown</span>
            </div>
        """, unsafe_allow_html=True)
        
        selected_subj = st.selectbox(
            "Select Subject to View:",
            options=sorted_subjects,
            index=0,
            key="home_subject_select_dropdown"
        )
        
        subj_data = curricula[selected_subj]
        subj_stats = calculate_subject_stats(subj_data)
        subj_code = subj_data.get("subject_code", "")
        subj_icon = subj_data.get("icon", "📚")
        
        s_pct = subj_stats.get("completion_pct", 0)
        s_avg = subj_stats.get("avg_score")
        if s_avg is not None:
            s_color = get_ragp_color(s_avg)
            s_color_hex = RAGP_HEX_MAP.get(s_color, "#94A3B8")
            s_badge_html = f'<span class="cat-score-badge" style="background: {s_color_hex}18; color: {s_color_hex}; border: 1px solid {s_color_hex}45; font-size: 0.8rem; padding: 0.15rem 0.55rem;">{s_avg}% • {s_color}</span>'
        else:
            s_badge_html = '<span class="cat-score-badge" style="background: #162032; color: #94A3B8; border: 1px solid #334155; font-size: 0.8rem; padding: 0.15rem 0.55rem;">Not Started</span>'
            
        st.progress(s_pct / 100.0)
        
        subj_overview_html = (
            f'<div class="home-stat-overview-box">'
            f'<div class="home-stat-row">'
            f'<span><b>{subj_icon} {selected_subj} Completion:</b></span>'
            f'<span style="font-weight: 800; color: #F8FAFC;">{subj_stats["completed"]} / {subj_stats["total"]} ({s_pct}%)</span>'
            f'</div>'
            f'<div class="home-stat-row" style="margin-bottom: 0;">'
            f'<span><b>Subject Average Score:</b></span>'
            f'<span>{s_badge_html}</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(subj_overview_html, unsafe_allow_html=True)
        
        s_ragp = subj_stats["ragp"]
        subj_ragp_html = (
            f'<div style="font-size: 0.74rem; font-weight: 700; color: #94A3B8; margin-bottom: 0.4rem;">{selected_subj} Mastery Breakdown:</div>'
            f'<div class="cat-rag-summary" style="margin-bottom: 1.1rem;">'
            f'{make_rag_tooltip_html("Pink", count=s_ragp["Pink"])}'
            f'{make_rag_tooltip_html("Green", count=s_ragp["Green"])}'
            f'{make_rag_tooltip_html("Amber", count=s_ragp["Amber"])}'
            f'{make_rag_tooltip_html("Red", count=s_ragp["Red"])}'
            f'{make_rag_tooltip_html("None", count=s_ragp.get("None", 0))}'
            f'</div>'
        )
        st.markdown(subj_ragp_html, unsafe_allow_html=True)
        
        # Last 3 lessons attempted
        recent_attempts = get_recent_subject_attempts(subj_data, limit=3)
        st.markdown('<div style="font-size: 0.88rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;"><span>⏱️</span><span>Last 3 Lessons Attempted</span></div>', unsafe_allow_html=True)
        
        if recent_attempts:
            items_html = ['<div class="home-recent-list">']
            for att in recent_attempts:
                att_score = att.get("score")
                att_color = att.get("color", "Green")
                att_chip = make_rag_tooltip_html(att_color, score=att_score, align="right")
                time_str = "Recently completed"
                if att.get("timestamp"):
                    try:
                        dt = datetime.fromisoformat(att["timestamp"])
                        time_str = dt.strftime("%d %b • %H:%M")
                    except Exception:
                        time_str = "Completed"
                        
                items_html.append(
                    f'<div class="home-recent-item">'
                    f'<div class="home-recent-info">'
                    f'<div class="home-recent-title" title="{att["title"]}">{att["title"]}</div>'
                    f'<div class="home-recent-meta"><span>{att.get("category", selected_subj)}</span> • <span>{time_str}</span></div>'
                    f'</div>'
                    f'<div>{att_chip}</div>'
                    f'</div>'
                )
            items_html.append('</div>')
            st.markdown("".join(items_html), unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="home-empty-attempts">
                <div style="font-size: 1.6rem; margin-bottom: 0.25rem;">📝</div>
                <div style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">No lessons attempted yet in {selected_subj}</div>
                <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.2rem;">Complete your first topic knowledge check to establish your diagnostic grade baseline!</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Call to Action: Start Studying link/button
        if st.button(f"🚀 Start Studying {selected_subj} ➔", key="home_start_study_cta_btn", use_container_width=True, type="primary"):
            target_tab = next((t for t in tab_titles if selected_subj in t), None)
            if target_tab:
                st.session_state["main_nav_radio"] = target_tab
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

CATEGORY_ICONS = {
    # Maths
    "Algebra": "🧮",
    "Geometry and Measures": "📐",
    "Number": "🔢",
    "Ratio and Proportion": "⚖️",
    "Probability": "🎲",
    "Statistics": "📊",
    # Biology
    "Cell Biology": "🔬",
    "Infection and Response": "🦠",
    "Bioenergetics": "🌿",
    "Homeostasis and Response": "🧠",
    "Inheritance & Evolution": "🧬",
    "Inheritance and Evolution": "🧬",
    "Inheritance, Variation and Evolution": "🧬",
    "Ecology": "🌍",
}

CATEGORY_DISPLAY_SHORT = {
    # Biology - compact display names guaranteed to fit on one line
    "Cell Biology": "🔬 Cell Bio",
    "Infection and Response": "🦠 Infection",
    "Bioenergetics": "🌿 Bioenergy",
    "Homeostasis and Response": "🧠 Homeostasis",
    "Inheritance & Evolution": "🧬 Genetics",
    "Inheritance and Evolution": "🧬 Genetics",
    "Ecology": "🌍 Ecology",
    # Maths
    "Algebra": "🧮 Algebra",
    "Geometry and Measures": "📐 Geometry",
    "Number": "🔢 Number",
    "Probability": "🎲 Probability",
    "Ratio and Proportion": "⚖️ Ratio",
    "Statistics": "📊 Statistics",
}

for idx, subject_name in enumerate(subject_names):
    if page_selection == tab_titles[idx + 1]:
        subj_data = curricula[subject_name]
        topics = subj_data.get("topics", [])
        
        # Calculate subject-specific stats
        subj_total = len(topics)
        subj_completed = sum(1 for t in topics if get_topic_progress(t["id"])["completed"])
        subj_red = [t for t in topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["color"] == "Red"]
        subj_pct = round((subj_completed / max(1, subj_total)) * 100, 1)

        # Ultra-compact native Streamlit header (zero raw code block issues, fits on screen)
        col_hdr_left, col_hdr_right = st.columns([6, 4])
        with col_hdr_left:
            st.markdown(f"### {subj_data.get('icon', '📚')} {subject_name} <span style='font-size:0.85rem; color:#94A3B8; font-weight:500;'>• AQA GCSE ({subj_data.get('subject_code', 'GCSE')})</span>", unsafe_allow_html=True)
        with col_hdr_right:
            tgt_badge = f" • <span style='color:#F87171; font-weight:700;'>🎯 {len(subj_red)} Target(s)</span>" if subj_red else ""
            st.markdown(f"<div style='text-align:right; font-size:0.8rem; font-weight:600; color:#94A3B8; margin-bottom:2px;'>Completed: <b style='color:#4ADE80;'>{subj_completed}/{subj_total}</b> ({subj_pct}%){tgt_badge}</div>", unsafe_allow_html=True)
            st.progress(subj_pct / 100.0)
        
        subj_tabs = st.tabs(["📚 Curriculum & Lessons", "🤖 Ask AI Tutor"])
        with subj_tabs[0]:
            # Group topics by Category with sanitized names (no rogue commas)
            categories = {}
            for t in topics:
                cat = t.get("category", "General")
                cat = cat.replace(", and ", " & ").replace(",", " &").strip()
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(t)
            cat_names = list(categories.keys())
            
            active_lesson_id = st.session_state.get(f"active_lesson_{subject_name}")

            if not active_lesson_id:
                # -------------------------------------------------
                # EXPANDED CATEGORY ROW WITH NAV ARROWS & SPLIT CARDS
                # (Image Left, Title / Completion / Score Bar Right)
                # -------------------------------------------------
                num_cats = len(cat_names)
                if f"cat_window_idx_{subject_name}" not in st.session_state:
                    st.session_state[f"cat_window_idx_{subject_name}"] = 0
                window_idx = st.session_state[f"cat_window_idx_{subject_name}"] % num_cats

                if f"selected_cat_{subject_name}" not in st.session_state or st.session_state[f"selected_cat_{subject_name}"] not in cat_names:
                    st.session_state[f"selected_cat_{subject_name}"] = cat_names[0]
                selected_cat = st.session_state[f"selected_cat_{subject_name}"]

                # Row of Categories flanked by Left and Right Arrow Paddles
                col_arr_prev, col_1, col_2, col_3, col_arr_next = st.columns([0.65, 3.55, 3.55, 3.55, 0.65])

                # Left cycling arrow (Cycles visible row without changing selected category)
                with col_arr_prev:
                    st.markdown('<div class="cat-arrow-spacer"></div>', unsafe_allow_html=True)
                    if st.button("◀", key=f"cat_row_prev_{subject_name}", help="Cycle categories left along the row", use_container_width=True):
                        st.session_state[f"cat_window_idx_{subject_name}"] = (window_idx - 1) % num_cats
                        st.rerun()

                # Right cycling arrow (Cycles visible row without changing selected category)
                with col_arr_next:
                    st.markdown('<div class="cat-arrow-spacer"></div>', unsafe_allow_html=True)
                    if st.button("▶", key=f"cat_row_next_{subject_name}", help="Cycle categories right along the row", use_container_width=True):
                        st.session_state[f"cat_window_idx_{subject_name}"] = (window_idx + 1) % num_cats
                        st.rerun()

                def render_split_category_card(target_col, c_idx):
                    c_name = cat_names[c_idx]
                    c_topics = categories[c_name]
                    c_tot = len(c_topics)
                    c_done = sum(1 for t in c_topics if get_topic_progress(t["id"])["completed"])
                    c_pct = round((c_done / max(1, c_tot)) * 100)

                    # Compute category average quiz score
                    scores = [get_topic_progress(t["id"])["score"] for t in c_topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["score"] is not None]
                    if scores:
                        avg_score = round(sum(scores) / len(scores))
                        avg_color = get_ragp_color(avg_score)
                        score_display = f"{avg_score}%"
                        score_color_hex = RAGP_HEX_MAP.get(avg_color, "#94A3B8")
                        score_bar_pct = avg_score
                        badge_html = f'<span class="cat-score-badge" style="background: {score_color_hex}18; color: {score_color_hex}; border: 1px solid {score_color_hex}45;">{avg_score}% • {avg_color}</span>'
                    else:
                        avg_score = None
                        avg_color = "None"
                        score_display = "—"
                        score_color_hex = "#334155"
                        score_bar_pct = 0
                        badge_html = '<span class="cat-score-badge" style="background: #162032; color: #94A3B8; border: 1px solid #334155;">Not Started</span>'

                    c_pink = sum(1 for t in c_topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["color"] == "Pink")
                    c_green = sum(1 for t in c_topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["color"] == "Green")
                    c_amber = sum(1 for t in c_topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["color"] == "Amber")
                    c_red = sum(1 for t in c_topics if get_topic_progress(t["id"])["completed"] and get_topic_progress(t["id"])["color"] == "Red")
                    c_none = c_tot - c_done
                    c_ico = CATEGORY_ICONS.get(c_name, "📚")

                    is_selected = (c_name == selected_cat)
                    active_class = "active" if is_selected else ""
                    tag_class = "active-tag" if is_selected else "click-tag"
                    tag_text = "✨ ACTIVE" if is_selected else "Click to View"
                    svg_img = get_category_svg(c_name)

                    with target_col:
                        card_html = (
                            f'<div class="cat-card-split {active_class}" onclick="const col = this.closest(\'.stColumn, [data-testid=column], [data-testid=stColumn], [data-testid=stHorizontalBlock] > div\'); if(col) {{ const btn = col.querySelector(\'button\'); if(btn) btn.click(); }}">'
                            f'<div class="cat-card-img-pane">{svg_img}</div>'
                            f'<div class="cat-card-data-pane">'
                            f'<div class="cat-card-top-row">'
                            f'<div class="cat-card-title-text" title="{c_name}">{c_ico} {c_name}</div>'
                            f'<span class="cat-card-tag {tag_class}">{tag_text}</span>'
                            f'</div>'
                            f'<div class="cat-stat-row">'
                            f'<span class="cat-stat-label">Completed</span>'
                            f'<span class="cat-stat-val"><b>{c_done}/{c_tot}</b> ({c_pct}%)</span>'
                            f'</div>'
                            f'<div class="cat-stat-row">'
                            f'<span class="cat-stat-label">Average Score</span>'
                            f'<span class="cat-stat-val">{badge_html}</span>'
                            f'</div>'
                            f'<div class="cat-avg-bar-track" title="Average Score: {score_display}">'
                            f'<div class="cat-avg-bar-fill" style="width: {score_bar_pct}%; background: {score_color_hex};"></div>'
                            f'</div>'
                            f'<div class="cat-rag-summary" onclick="const col = this.closest(\'.stColumn, [data-testid=column], [data-testid=stColumn], [data-testid=stHorizontalBlock] > div\'); if(col) {{ const btn = col.querySelector(\'button\'); if(btn) btn.click(); }}">'
                            f'{make_rag_tooltip_html("Pink", count=c_pink)}'
                            f'{make_rag_tooltip_html("Green", count=c_green)}'
                            f'{make_rag_tooltip_html("Amber", count=c_amber)}'
                            f'{make_rag_tooltip_html("Red", count=c_red)}'
                            f'{make_rag_tooltip_html("None", count=c_none)}'
                            f'</div>'
                            f'</div>'
                            f'</div>'
                        )
                        st.markdown(card_html, unsafe_allow_html=True)

                        # Invisible full-card overlay button that activates on clicking anywhere on the card
                        if st.button("", key=f"select_cat_{subject_name}_{c_idx}", help=f"Click to select {c_name} and view lessons", use_container_width=True):
                            st.session_state[f"selected_cat_{subject_name}"] = c_name
                            st.rerun()

                # Render 3 visible category cards
                render_split_category_card(col_1, (window_idx + 0) % num_cats)
                render_split_category_card(col_2, (window_idx + 1) % num_cats)
                render_split_category_card(col_3, (window_idx + 2) % num_cats)

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                
                # -------------------------------------------------
                # SELECTABLE CARDS BENEATH (Lessons in Selected Category)
                # -------------------------------------------------
                selected_topics = categories.get(selected_cat, [])
                header_html = (
                    f'<div class="lesson-grid-header">'
                    f'<div style="font-size: 0.95rem; font-weight: 800; color: #F8FAFC; display: flex; align-items: center; gap: 0.4rem;">'
                    f'<span>📂</span>'
                    f'<span>{selected_cat} Lessons</span>'
                    f'<span style="font-size: 0.74rem; font-weight: 700; color: #FB7185; background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.35); padding: 0.1rem 0.5rem; border-radius: 999px;">'
                    f'{len(selected_topics)} Lessons'
                    f'</span>'
                    f'</div>'
                    f'<div class="rag-guide-strip" style="margin-bottom:0;">'
                    f'<span class="rag-guide-title">Hover RAGP Guide:</span>'
                    f'{make_rag_tooltip_html("Pink", label_override="🌸 100% Perfect")}'
                    f'{make_rag_tooltip_html("Green", label_override="🟢 ≥70% Mastered")}'
                    f'{make_rag_tooltip_html("Amber", label_override="🟡 50–69% Revising")}'
                    f'{make_rag_tooltip_html("Red", label_override="🔴 <50% Focus")}'
                    f'{make_rag_tooltip_html("None", label_override="⚪ Unattempted")}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(header_html, unsafe_allow_html=True)
                
                # Render in a clean 3-column responsive grid
                lesson_cols = st.columns(3)
                for i, t in enumerate(selected_topics):
                    with lesson_cols[i % 3]:
                        prog = get_topic_progress(t["id"])
                        is_done = prog["completed"]
                        score_val = prog["score"]
                        rag_color = prog["color"]
                        
                        if is_done and score_val is not None:
                            score_badge = make_rag_tooltip_html(rag_color, score=score_val, align="right")
                        else:
                            score_badge = make_rag_tooltip_html("None", align="right")
                            
                        tier_label = t.get("tier", "GCSE")
                        mins = t.get("estimated_mins", 25)
                        
                        lesson_card_html = (
                            f'<div class="lesson-card-box">'
                            f'<div>'
                            f'<div class="lesson-card-title">{t["title"]}</div>'
                            f'<div class="lesson-meta-row">'
                            f'<span style="font-weight:700; color:#FB7185;">{tier_label}</span>'
                            f'<span>⏱️ {mins}m</span>'
                            f'</div>'
                            f'</div>'
                            f'<div style="margin-top: 0.35rem; display: flex; align-items: center; justify-content: flex-end;">'
                            f'{score_badge}'
                            f'</div>'
                            f'</div>'
                        )
                        st.markdown(lesson_card_html, unsafe_allow_html=True)
                        
                        btn_txt = "Review Lesson ➔" if is_done else "Start Lesson ➔"
                        if st.button(btn_txt, key=f"start_{t['id']}", use_container_width=True):
                            st.session_state[f"active_lesson_{subject_name}"] = t["id"]
                            st.rerun()

            else:
                # -------------------------------------------------
                # LESSON DETAIL VIEW (Compact & Fit on Page)
                # -------------------------------------------------
                lesson = next((t for t in topics if t["id"] == active_lesson_id), None)
                if lesson:
                    lesson_cat = lesson.get("category", "Categories")
                    
                    # Top action bar
                    col_b1, col_b2 = st.columns([2.5, 7.5])
                    with col_b1:
                        if st.button(f"⬅ Back to {lesson_cat}", key=f"back_{subject_name}", use_container_width=True):
                            st.session_state[f"active_lesson_{subject_name}"] = None
                            st.rerun()
                    with col_b2:
                        prog = get_topic_progress(lesson["id"])
                        status_badge = make_rag_tooltip_html(prog['color'] if prog['score'] is not None else 'None', score=prog['score'], align='right')
                        st.markdown(f"""
                        <div style="display:flex; align-items:center; justify-content:space-between; padding:0.25rem 0;">
                          <div style="font-size:1.15rem; font-weight:800; color:#F8FAFC;">📖 {lesson['title']}</div>
                          <div style="font-size:0.8rem; color:#94A3B8; display:flex; align-items:center; gap:0.4rem;">Status: {status_badge}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    objs = " • ".join(lesson.get("objectives", []))
                    if objs:
                        st.caption(f"🎯 **Objectives:** {objs}")
                        
                    lesson_tabs = st.tabs(["📚 Notes & Slides", "✅ Knowledge Check"])
                    
                    # Tab 1: Notes & Slides
                    with lesson_tabs[0]:
                        concept = lesson.get("concept_breakdown", {})
                        if concept.get("summary"):
                            st.info(concept.get("summary"))
                            
                        slides = lesson.get("detailed_slides", concept.get("key_rules", []))
                        if not slides:
                            slides = ["No specific notes provided."]
                            
                        slide_idx = st.session_state.get(f"slide_{lesson['id']}", 0)
                        slide_idx = min(max(0, slide_idx), len(slides) - 1)
                        
                        subject_class = "biology" if "Biology" in subject_name else "maths" if "Math" in subject_name else ""
                        
                        # Compact Slide View Container
                        st.markdown(f'<div class="slide-card {subject_class}" style="min-height:240px; max-height:360px; overflow-y:auto;">\n\n{slides[slide_idx]}\n\n</div>', unsafe_allow_html=True)
                        st.write("")
                        
                        col_prev, col_slide_info, col_next = st.columns([1.5, 3, 1.5])
                        with col_prev:
                            if st.button("⬅️ Prev Slide", key=f"prev_{lesson['id']}", disabled=(slide_idx == 0), use_container_width=True):
                                st.session_state[f"slide_{lesson['id']}"] = slide_idx - 1
                                st.rerun()
                        with col_slide_info:
                            st.markdown(f"<div style='text-align:center; font-weight:700; color:#94A3B8; padding-top:0.4rem;'>Slide {slide_idx + 1} of {len(slides)}</div>", unsafe_allow_html=True)
                        with col_next:
                            if st.button("Next Slide ➡️", key=f"next_{lesson['id']}", disabled=(slide_idx == len(slides) - 1), use_container_width=True):
                                st.session_state[f"slide_{lesson['id']}"] = slide_idx + 1
                                st.rerun()
                                
                        # Worked Example in Collapsible Section to save screen space
                        worked = lesson.get("worked_example", {})
                        if worked.get("question"):
                            with st.expander(f"🧑‍🏫 Worked Example: {worked.get('question')} [{worked.get('marks', 0)} marks]"):
                                for s in worked.get("steps", []):
                                    st.markdown(f"**Step {s.get('step')}:** {s.get('explanation')}")
                                    
                    # Tab 2: Knowledge Check Quiz
                    with lesson_tabs[1]:
                        quiz_bank = lesson.get("quiz_bank", [])
                        if not quiz_bank:
                            st.warning("No quiz available for this lesson.")
                        else:
                            st.markdown(f"### 📝 10-Question Knowledge Check (Topic: {lesson['title']})")
                            
                            if f"quiz_active_{lesson['id']}" not in st.session_state:
                                if st.button("Start Knowledge Check", key=f"btn_start_quiz_{lesson['id']}"):
                                    st.session_state[f"quiz_active_{lesson['id']}"] = True
                                    st.session_state[f"quiz_data_{lesson['id']}"] = generate_quiz(quiz_bank, 10)
                                    st.session_state[f"quiz_answers_{lesson['id']}"] = {}
                                    st.rerun()
                                    
                            if st.session_state.get(f"quiz_active_{lesson['id']}"):
                                q_data = st.session_state[f"quiz_data_{lesson['id']}"]
                                for i, q in enumerate(q_data):
                                    st.markdown(f"**Q{i+1}: {q['question']}**")
                                    ans = st.radio(
                                        "Select Answer:",
                                        q["options"],
                                        index=None,
                                        key=f"q_{lesson['id']}_{i}"
                                    )
                                    if ans:
                                        st.session_state[f"quiz_answers_{lesson['id']}"][i] = q["options"].index(ans)
                                        
                                if st.button("Submit Quiz", key=f"submit_quiz_{lesson['id']}"):
                                    results = evaluate_quiz(q_data, st.session_state[f"quiz_answers_{lesson['id']}"])
                                    pct = results["pct"]
                                    update_topic_quiz_score(lesson["id"], pct)
                                    
                                    color = get_ragp_color(pct)
                                    st.success(f"You scored {pct}%! Grade: {color}")
                                    
                                    for r in results["breakdown"]:
                                        if r["correct"]:
                                            st.write(f"✅ {r['question']} - Correct")
                                        else:
                                            correct_ans = r["options"][r["answer_index"]]
                                            st.write(f"❌ {r['question']} - Incorrect. Correct answer: {correct_ans}")
                                            
                                    del st.session_state[f"quiz_active_{lesson['id']}"]
                                    if st.button("Close Results", key=f"close_results_{lesson['id']}"):
                                        st.rerun()


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

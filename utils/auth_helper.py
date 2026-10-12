import os
import streamlit as st
from typing import Optional

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")

# Fallback plain-text accounts (used when streamlit_authenticator is unavailable)
FALLBACK_ACCOUNTS = {
    "lizalou7@icloud.com":     {"password": "21062011",  "name": "Liza",   "role": "student"},
    "emmandhoward@aol.com":    {"password": "26111968",  "name": "Emma",   "role": "student"},
    "emmandhoward@aol.co.uk":  {"password": "03011971",  "name": "Howard", "role": "student"},
    "mstiles11@icloud.com":    {"password": "06122006",  "name": "Matt",   "role": "student"},
}


def load_auth_config() -> Optional[dict]:
    try:
        import yaml
        from yaml.loader import SafeLoader
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=SafeLoader)
    except Exception:
        pass
    return None


def get_authenticator():
    try:
        import streamlit_authenticator as stauth
        config = load_auth_config()
        if not config:
            return None, False
        try:
            auth = stauth.Authenticate(
                config.get("credentials", {}),
                config.get("cookie", {}).get("name", "gcse_cookie"),
                config.get("cookie", {}).get("key", "secret"),
                config.get("cookie", {}).get("expiry_days", 30),
                config.get("pre-authorized", {}).get("emails", []),
            )
            return auth, True
        except TypeError:
            auth = stauth.Authenticate(
                config.get("credentials", {}),
                config.get("cookie", {}).get("name", "gcse_cookie"),
                config.get("cookie", {}).get("key", "secret"),
                config.get("cookie", {}).get("expiry_days", 30),
            )
            return auth, True
    except ImportError:
        return None, False
    except Exception:
        return None, False


def render_login_page(authenticator=None, has_stauth: bool = False) -> bool:
    """Renders the login UI. Returns True when authenticated."""
    if st.session_state.get("authentication_status") is True:
        return True

    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1.5rem;">
        <div style="font-size:3.5rem; margin-bottom:0.5rem;">🎓</div>
        <h1 style="margin:0; font-family:'Inter',sans-serif; font-weight:800;
                   background:linear-gradient(135deg,#6366F1,#8B5CF6,#A855F7);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            GCSE Revision Master
        </h1>
        <p style="color:#94A3B8; margin-top:0.4rem; font-size:1.05rem;">
            Sign in to access your personalised revision portal
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        # Try official streamlit_authenticator widget first
        if has_stauth and authenticator is not None:
            try:
                authenticator.login(location="main")
                status = st.session_state.get("authentication_status")
                if status is False:
                    st.error("❌ Incorrect email or password. Please try again.")
                elif status is None:
                    st.info("Enter your email address and password to sign in.")
                return bool(status)
            except Exception:
                pass  # fall through to fallback form

        # Built-in fallback form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 🔐 Sign In")
            email = st.text_input("Email Address", placeholder="your@email.com").strip().lower()
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                if email in FALLBACK_ACCOUNTS and FALLBACK_ACCOUNTS[email]["password"] == password:
                    user = FALLBACK_ACCOUNTS[email]
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = email
                    st.session_state["name"] = user["name"]
                    st.session_state["role"] = user["role"]
                    st.success(f"✅ Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.session_state["authentication_status"] = False
                    st.error("❌ Incorrect email or password.")

    return st.session_state.get("authentication_status") is True


def logout():
    for key in ["authentication_status", "username", "name", "role", "user_progress", "question_submissions"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def render_user_header(authenticator=None):
    """Renders candidate header with greeting, target grade, and horizontal logout button."""
    name = st.session_state.get("name", "Student")
    username = st.session_state.get("username", "student")
    role = st.session_state.get("role", "student").title()
    
    target_grade = st.session_state.get("target_grade")
    if not target_grade:
        # Fallback to config if not in session
        try:
            import yaml
            with open("config.yaml", "r") as f:
                c = yaml.safe_load(f)
            target_grade = c["credentials"]["usernames"][username].get("target_grade", "8")
        except:
            target_grade = "8"
        st.session_state["target_grade"] = target_grade

    initials = "".join([n[0] for n in name.split()[:2]]).upper() if name else "S"
    profile_html = f"""
    <div class="user-profile-card">
        <div class="profile-avatar">{initials}</div>
        <div class="profile-details">
            <div class="profile-name">{name}</div>
            <div class="profile-meta">{role} &bull; Target: Grade {target_grade}</div>
        </div>
    </div>
    """
    st.sidebar.markdown(profile_html, unsafe_allow_html=True)
    
    if st.sidebar.button("⚙️ Edit Profile Details", use_container_width=True):
        st.session_state["page"] = "profile"
        st.rerun()
    if st.sidebar.button("🚪 Logout", key="logout_button_nav", help="Sign out of GCSE portal", use_container_width=True):
        if authenticator is not None:
            try:
                pass
            except Exception:
                pass
        logout()
    st.sidebar.markdown("---")

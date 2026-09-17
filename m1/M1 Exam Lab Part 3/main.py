import streamlit as st
from models import SystemManager
from views import AppViews

st.set_page_config(page_title="PeerEval Prototype", page_icon="🎓", layout="centered")

def init_session():
    if "sys_manager" not in st.session_state:
        st.session_state["sys_manager"] = SystemManager()
    if "step" not in st.session_state:
        st.session_state["step"] = "login"
    if "logged_user" not in st.session_state:
        st.session_state["logged_user"] = None

def render_sidebar():
    st.sidebar.title("📌 PeerEval Navigation")
    st.sidebar.write("User Journey Tracker:")

    steps = [
        ("1. Open App", "login"),
        ("2. Log In", "login"),
        ("3. Access Dashboard", "dashboard"),
        ("4. Select Group & Task", "project_group"),
        ("5. Fill Evaluation", "evaluation_form"),
        ("6. Save & Submit", "evaluation_form"),
        ("7. View Updated Status", "confirmation"),
    ]

    current_step = st.session_state["step"]
    for label, step_key in steps:
        if current_step == step_key:
            st.sidebar.markdown(f"👉 **{label}**")
        else:
            st.sidebar.markdown(f"⚪ {label}")

    st.sidebar.markdown("---")
    if st.session_state["logged_user"]:
        st.sidebar.write(f"**Logged in:** {st.session_state['logged_user'].get_name()}")
        if st.sidebar.button("Step 8: Log Out"):
            st.session_state["logged_user"] = None
            st.session_state["step"] = "login"
            st.rerun()

def main():
    init_session()
    render_sidebar()

    st.title("🎓 PeerEval Prototype")
    st.caption("Student Group Project & Peer Evaluation System")
    st.markdown("---")

    sys_manager = st.session_state["sys_manager"]
    current_step = st.session_state["step"]

    if current_step == "login":
        AppViews.render_login(sys_manager)
    elif current_step == "dashboard":
        AppViews.render_dashboard()
    elif current_step == "project_group":
        AppViews.render_project_group(sys_manager)
    elif current_step == "evaluation_form":
        AppViews.render_evaluation_form(sys_manager)
    elif current_step == "confirmation":
        AppViews.render_confirmation(sys_manager)

if __name__ == "__main__":
    main()
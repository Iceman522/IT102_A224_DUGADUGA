import streamlit as st
from models import SystemManager, PeerEvaluation

class AppViews:
    @staticmethod
    def render_login(sys_manager: SystemManager):
        st.header("🔑 Step 2: Register or Log In")
        st.write("Welcome to **PeerEval**! Please select your role and log in.")

        role = st.selectbox("Select Role", ["Student", "Instructor"])
        
        if role == "Student":
            st.info("Demo Student Credentials: ID = **S101**, **S102**, or **S103**")
            user_id = st.text_input("Enter Student ID", value="S101")
        else:
            st.info("Demo Instructor Credential: ID = **I201**")
            user_id = st.text_input("Enter Instructor ID", value="I201")

        if st.button("Log In"):
            user = sys_manager.authenticate(user_id, role)
            if user:
                st.session_state["logged_user"] = user
                st.session_state["step"] = "dashboard"
                st.rerun()
            else:
                st.error("Invalid ID provided. Please try again.")

    @staticmethod
    def render_dashboard():
        user = st.session_state["logged_user"]
        st.header("📊 Step 3: Access Dashboard")
        st.success(f"Logged in as: **{user.get_name()}** ({user.get_role()})")

        st.subheader("Your Active Courses & Projects")
        st.write("- **IS102: Object-Oriented Programming** — *Semester Project*")

        if user.get_role() == "Student":
            st.info(f"Assigned Group: **{user.group_id}**")
            if st.button("Go to Project Group"):
                st.session_state["step"] = "project_group"
                st.rerun()
        else:
            st.info("Instructor Overview Mode")
            st.write("Total Peer Submissions Pending: **3**")

    @staticmethod
    def render_project_group(sys_manager: SystemManager):
        user = st.session_state["logged_user"]
        st.header("👥 Step 4: Access Project Group & Tasks")

        group = sys_manager.get_group(user.group_id)
        if group:
            st.subheader(f"{group.group_name}")
            st.write("**Group Members:**")
            for member_id in group.members:
                member_name = sys_manager.students[member_id].get_name()
                st.write(f"- {member_name} ({member_id})")

            st.markdown("---")
            st.write("📌 **Pending Task:** Midterm Peer Evaluation Rubric")
            
            if st.button("Start Peer Evaluation"):
                st.session_state["step"] = "evaluation_form"
                st.rerun()

    @staticmethod
    def render_evaluation_form(sys_manager: SystemManager):
        user = st.session_state["logged_user"]
        st.header("📝 Step 5 & 6: Fill Out and Submit Evaluation")

        group = sys_manager.get_group(user.group_id)
        teammates = [m for m in group.members if m != user.get_id()]

        st.write("Assess your team members on collaboration, communication, and code contribution.")

        target_id = st.selectbox(
            "Select Teammate to Evaluate",
            teammates,
            format_func=lambda x: f"{sys_manager.students[x].get_name()} ({x})"
        )

        score = st.slider("Rating Score (1 - Poor, 10 - Excellent)", 1, 10, 8)
        comments = st.text_area("Provide Constructive Feedback / Comments", "Great work on implementing modular classes!")

        if st.button("Save & Submit Information"):
            eval_record = PeerEvaluation(user.get_id(), target_id, score, comments)
            sys_manager.submit_evaluation(eval_record)
            st.session_state["last_eval"] = eval_record
            st.session_state["step"] = "confirmation"
            st.rerun()

    @staticmethod
    def render_confirmation(sys_manager: SystemManager):
        st.header("✅ Step 7: View Updated Status")
        st.success("Peer evaluation successfully submitted and recorded!")

        last_eval = st.session_state.get("last_eval")
        if last_eval:
            target_name = sys_manager.students[last_eval.evaluatee_id].get_name()
            st.subheader("Submitted Details Summary:")
            st.json({
                "Evaluator": st.session_state["logged_user"].get_name(),
                "Evaluatee": target_name,
                "Score Assigned": f"{last_eval.score} / 10",
                "Feedback": last_eval.comments
            })

        if st.button("Return to Dashboard"):
            st.session_state["step"] = "dashboard"
            st.rerun()
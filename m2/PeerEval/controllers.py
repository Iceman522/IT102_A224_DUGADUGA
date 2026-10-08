import streamlit as st
from models import Student, Instructor, ProjectGroup, PeerEvaluation, GroupHealthAnalyzer, DataStorage
import views

class AppController:
    def __init__(self):
        self._init_session_state()
        self.analyzer = GroupHealthAnalyzer()

    def _init_session_state(self):
        if "current_user" not in st.session_state:
            st.session_state.current_user = None

        if "active_nav" not in st.session_state:
            st.session_state.active_nav = "Evaluate"

        if "evaluations" not in st.session_state:
            loaded_evals = DataStorage.load_evaluations()
            if loaded_evals:
                st.session_state.evaluations = loaded_evals
            else:
                st.session_state.evaluations = [
                    PeerEvaluation("e1", "S101", "S102", 5, 5, 5, "Great work!"),
                    PeerEvaluation("e2", "S101", "S103", 2, 2, 1, "Unequal task share."),
                ]
                DataStorage.save_evaluations(st.session_state.evaluations)

        if "sample_group" not in st.session_state:
            student_user = Student(user_id="S2024-8921", name="Elena Rostova", role="Student", group_id="G4")
            st.session_state.sample_group = ProjectGroup(
                group_id="G4",
                group_name="Web Systems",
                members=[
                    student_user,
                    Student(user_id="S2024-102", name="Marcus Chen", role="Student", group_id="G4"),
                    Student(user_id="S2024-103", name="David Kim", role="Student", group_id="G4"),
                    Student(user_id="S2024-104", name="Priya Patel", role="Student", group_id="G4")
                ]
            )

    def run(self):
        if st.session_state.current_user is None:
            views.render_login_view(self.handle_login)
        else:
            user = st.session_state.current_user
            group = st.session_state.sample_group
            evals = st.session_state.evaluations
            health_report = self.analyzer.analyze_health(group.members, evals)

            # Route by active screen tab
            if st.session_state.active_nav == "Evaluate":
                other_members = [m for m in group.members if m.user_id != user.user_id]
                views.render_evaluation_form(group, other_members, self.handle_submit_evaluation)

            elif st.session_state.active_nav == "Health":
                views.render_group_health_view(health_report)

            elif st.session_state.active_nav == "Reports":
                views.render_instructor_report(user, group, evals, health_report)

            elif st.session_state.active_nav == "Account":
                st.title("👤 User Account & Session")
                st.info(f"Logged in as: **{user.name}** ({user.user_id})")
                if st.button("Logout"):
                    self.handle_logout()

            # Render Bottom Navigation Bar
            new_nav = views.render_bottom_nav(st.session_state.active_nav)
            if new_nav != st.session_state.active_nav:
                st.session_state.active_nav = new_nav
                st.rerun()

    def handle_login(self, role: str, user_id: str):
        if role == "Student":
            st.session_state.current_user = Student(user_id=user_id, name="Elena Rostova", role="Student", group_id="G4")
            st.session_state.active_nav = "Evaluate"
        else:
            st.session_state.current_user = Instructor(user_id=user_id, name="Dr. Smith", role="Instructor", department="IS")
            st.session_state.active_nav = "Reports"
        st.rerun()

    def handle_logout(self):
        st.session_state.current_user = None
        st.rerun()

    def handle_submit_evaluation(self, target_id: str, comm: int, effort: int, tech: int, feedback: str):
        evaluator_id = st.session_state.current_user.user_id
        new_eval = PeerEvaluation(
            eval_id=f"e{len(st.session_state.evaluations)+1}",
            evaluator_id=evaluator_id,
            evaluatee_id=target_id,
            communication_score=comm,
            effort_score=effort,
            technical_score=tech,
            feedback=feedback
        )
        st.session_state.evaluations.append(new_eval)
        DataStorage.save_evaluations(st.session_state.evaluations)
        st.rerun()
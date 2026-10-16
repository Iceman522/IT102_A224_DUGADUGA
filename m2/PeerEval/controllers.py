import streamlit as st
from models import Student, Instructor, ProjectGroup, PeerEvaluation, GroupHealthAnalyzer, DataStorage
import views

class AppController:
    def __init__(self):
        # Initialize SQLite database
        DataStorage.initialize_db()
        
        # Initialize session state variables if not already present
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "current_user" not in st.session_state:
            st.session_state.current_user = None
        if "current_group" not in st.session_state:
            st.session_state.current_group = None
        if "current_tab" not in st.session_state:
            st.session_state.current_tab = "Evaluate"

    def run(self):
        # 1. Check Authentication State
        if not st.session_state.logged_in:
            views.render_login_view(self.handle_login)
            return

        user = st.session_state.current_user
        group = st.session_state.current_group
        
        # Load evaluations from SQLite database
        evaluations = DataStorage.load_evaluations()
        
        # Run DSS analysis on current group evaluations
        analyzer = GroupHealthAnalyzer()
        group_members = group.members if group else []
        health_report = analyzer.analyze_health(group_members, evaluations)

        # 2. Render View Based on Active Tab & Enforce Role-Based Access Control (RBAC)
        tab = st.session_state.current_tab
        
        # Security Guard: If student tries to access Reports, redirect them to Health
        if isinstance(user, Student) and tab == "Reports":
            tab = "Health"
            st.session_state.current_tab = "Health"

        # Security Guard: If instructor tries to access Evaluate, redirect them to Reports
        if isinstance(user, Instructor) and tab == "Evaluate":
            tab = "Reports"
            st.session_state.current_tab = "Reports"

        if tab == "Evaluate" and isinstance(user, Student):
            other_members = [m for m in group.members if m.user_id != user.user_id] if group else []
            views.render_evaluation_form(group, other_members, self.handle_submit_eval)
        elif tab == "Health":
            views.render_group_health_view(health_report)
        elif tab == "Reports" and isinstance(user, Instructor):
            views.render_instructor_report(user, group, evaluations, health_report)
        elif tab == "Account":
            views.render_profile_view(user, group, self.handle_logout)
        else:
            # Fallback default view based on role
            if isinstance(user, Instructor):
                views.render_instructor_report(user, group, evaluations, health_report)
            else:
                views.render_group_health_view(health_report)

        # 3. Render Bottom Navigation Bar with Strict Role Filtering
        selected_tab = views.render_bottom_nav_for_role(st.session_state.current_tab, user.role)
        if selected_tab != st.session_state.current_tab:
            st.session_state.current_tab = selected_tab
            st.rerun()

    def handle_login(self, role: str, user_id: str):
        """Handles user sign-in logic and mocks relational user objects."""
        st.session_state.logged_in = True
        
        if role == "Instructor":
            st.session_state.current_user = Instructor(
                user_id=user_id, 
                name="Dr. Alan Grant", 
                role="Instructor", 
                department="Information Systems"
            )
            st.session_state.current_group = ProjectGroup(
                group_id="G-Cohort", 
                group_name="IS 301 - Section A", 
                members=[]
            )
            st.session_state.current_tab = "Reports"  # Default landing for instructors
        else:
            st.session_state.current_user = Student(
                user_id=user_id, 
                name="Adrian Dugaduga", 
                role="Student", 
                group_id="G4"
            )
            st.session_state.current_group = ProjectGroup(
                group_id="G4", 
                group_name="Group 4 • Web Systems", 
                members=[
                    Student("S2024-8921", "Adrian Dugaduga", "Student", "G4"),
                    Student("S2024-8922", "Marcus Chen", "Student", "G4"),
                    Student("S2024-8923", "Elena Rostova", "Student", "G4"),
                    Student("S2024-8924", "David Kim", "Student", "G4")
                ]
            )
            st.session_state.current_tab = "Evaluate"  # Default landing for students

        st.rerun()

    def handle_submit_eval(self, evaluatee_id: str, comm: int, effort: int, tech: int, feedback: str):
        """Processes and saves a new peer evaluation to SQLite storage."""
        user = st.session_state.current_user
        eval_id = f"EV-{user.user_id}-{evaluatee_id}"
        
        new_eval = PeerEvaluation(
            eval_id=eval_id,
            evaluator_id=user.user_id,
            evaluatee_id=evaluatee_id,
            communication_score=comm,
            effort_score=effort,
            technical_score=tech,
            feedback=feedback
        )
        DataStorage.save_evaluation(new_eval)

    def handle_logout(self):
        """Clears session state and returns to login view."""
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.current_group = None
        st.session_state.current_tab = "Evaluate"
        st.rerun()
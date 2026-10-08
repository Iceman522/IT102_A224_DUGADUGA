import streamlit as st
import pandas as pd
from typing import List, Callable

# Inject CSS targeting Streamlit's structural layout
def inject_custom_css():
    st.markdown("""
    <style>
    /* Remove default Streamlit top padding and header bar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 500px !important;  /* Centers and bounds app width like a mobile/card view */
    }

    /* Global background */
    .stApp {
        background-color: #f6f8fe !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Card Container */
    .peereval-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
        border: 1px solid #eef2ff;
    }

    /* Force clean text styling on labels and inputs */
    label, .stRadio label, p, span {
        color: #1e293b !important;
        font-weight: 500;
    }

    /* Input Fields */
    .stTextInput input {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    /* Badges */
    .badge-purple {
        background-color: #4f46e5;
        color: white !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .badge-soft-blue {
        background-color: #e0e7ff;
        color: #3730a3 !important;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-green {
        background-color: #d1fae5;
        color: #065f46 !important;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }

    .badge-red {
        background-color: #fee2e2;
        color: #991b1b !important;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4f46e5 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
    }

    /* Metric Boxes */
    .metric-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #eef2ff;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 1. SCREEN 1: LOGIN
# ==========================================
def render_login_view(on_login_click: Callable):
    inject_custom_css()
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 16px;">
            <div style="background-color: #4f46e5; width: 56px; height: 56px; border-radius: 16px; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 28px;">💬</div>
            <h2 style="margin: 10px 0 0 0; font-size: 26px; color: #1e1b4b;">PeerEval <span class="badge-purple">v2.4 DSS</span></h2>
            <p style="color: #64748b !important; font-size: 12px; margin-top: 4px;">Decision Support System for Academic Peer Evaluations</p>
        </div>
    """, unsafe_allow_html=True)

    # Clean Card View
    with st.container():
        st.caption("EVALUATION ROLE")
        role_tab = st.radio("Select Role", ["🎓 Student", "📊 Instructor"], horizontal=True, label_visibility="collapsed")
        selected_role = "Student" if "Student" in role_tab else "Instructor"
        
        st.markdown("""
            <div style="background-color: #f1f5f9; padding: 8px 12px; border-radius: 8px; font-size: 12px; color: #334155; margin: 12px 0;">
                🟢 <b>Fall Term Cohort A-14</b> <span style="float: right; color: #64748b;">Active Window</span>
            </div>
        """, unsafe_allow_html=True)

        user_id = st.text_input("University / Student ID", value="S2024-8921" if selected_role == "Student" else "I2024-101", placeholder="e.g., S2024-8921")
        password = st.text_input("Password or Key", value="password", type="password", placeholder="Enter institutional password")
        
        st.checkbox("Remember device", value=True)

        if st.button("Sign In to Workspace ➔", use_container_width=True):
            on_login_click(selected_role, user_id)

        st.markdown("""
            <div style="text-align: center; margin: 12px 0; color: #94a3b8; font-size: 11px;">OR INSTITUTIONAL</div>
        """, unsafe_allow_html=True)
        
        st.button("🏛️ Log in with Campus SSO", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Footer Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="metric-box">
                <span style="font-size: 10px; color: #64748b;">🛡️ System Health</span>
                <div style="font-size: 15px; font-weight: bold; color: #0f172a;">99.98% <span style="font-size: 10px; color: #10b981;">Optimal</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-box">
                <span style="font-size: 10px; color: #64748b;">⚡ Telemetry Sync</span>
                <div style="font-size: 15px; font-weight: bold; color: #0f172a;">34ms <span style="font-size: 10px; color: #64748b;">Low Latency</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; font-size: 11px; color: #64748b !important; margin-top: 16px;">
            🔒 FERPA Compliant • End-to-End Encrypted Rubrics
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 2. SCREEN 2: EVALUATION FORM
# ==========================================
def render_evaluation_form(group, other_members: List, on_submit_eval: Callable):
    inject_custom_css()
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 11px; color: #64748b;">CS440 • FALL 2024</span>
                <h3 style="margin: 0; color: #0f172a;">Group 4 • Web Systems</h3>
                <span style="font-size: 11px; color: #64748b;">Sprint 3: Final Architectural Integration</span>
            </div>
            <span class="badge-red">⏰ Due in 18h</span>
        </div>
        <div class="peereval-card" style="background-color: #e0e7ff; border: none; padding: 12px; margin-top: 12px;">
            <div style="font-size: 12px; font-weight: 600; color: #3730a3 !important;">🛡️ Strictly Confidential DSS Protocol</div>
            <div style="font-size: 11px; color: #4338ca !important;">Individual scores are anonymized. Aggregated vectors feed decision telemetry.</div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("SELECT PEER TO REVIEW")
    
    if not other_members:
        st.info("No active teammates available for review.")
        return

    selected_peer = st.selectbox("Teammate", options=other_members, format_func=lambda x: f"{x.name} ({x.user_id})")

    st.markdown(f"""
        <div class="peereval-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #0f172a;">{selected_peer.name} <span class="badge-green">Active</span></h4>
                    <span style="font-size: 11px; color: #64748b;">Lead UI Architecture & State Sync</span>
                </div>
                <div style="text-align: right; font-size: 11px; color: #4f46e5; font-weight: 600;">14 PRs Merged</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Diagnostic Rubric")

    with st.form("rubric_form"):
        comm_score = st.slider("💬 Communication & Responsiveness", 1, 5, 5)
        st.caption("5 - Consistently prompt, proactive & facilitates team discussion")
        
        effort_score = st.slider("💎 Effort & Reliability", 1, 5, 4)
        st.caption("4 - Meets all deadlines with solid output & steady pace")

        tech_score = st.slider("⚙️ Technical Quality & Deliverables", 1, 5, 4)
        st.caption("4 - Significant high-quality code contributions & PR reviews")

        st.markdown("---")
        feedback = st.text_area("🔒 Confidential Peer Remarks (Instructor & DSS Only)", placeholder="Highlight collaboration strengths, blockers resolved, or key modules co-engineered...")

        col1, col2 = st.columns(2)
        with col1:
            st.form_submit_button("💾 Save Draft", use_container_width=True)
        with col2:
            submit = st.form_submit_button("✈️ Submit Rating", use_container_width=True)
            if submit:
                on_submit_eval(selected_peer.user_id, comm_score, effort_score, tech_score, feedback)
                st.success("Rating submitted successfully!")


# ==========================================
# 3. SCREEN 3: GROUP HEALTH CHECK
# ==========================================
def render_group_health_view(health_report: dict):
    inject_custom_css()

    st.markdown("""
        <div class="peereval-card" style="background-color: #e0e7ff; border: none;">
            <div style="font-weight: bold; color: #3730a3 !important; font-size: 15px;">💬 EvalBot Health Synthesis <span class="badge-purple">DSS v2.4</span></div>
            <div style="font-size: 12px; color: #4338ca !important; margin-top: 4px;">Peer feedback round complete. 1 structural variance outlier flagged for faculty intervention.</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-box">
                <div style="font-size: 10px; color: #64748b;">TEAM HEALTH</div>
                <div style="font-size: 22px; font-weight: bold; color: #0f172a;">{int(health_report['avg_score']*20)}% <span style="font-size: 12px; color: #10b981;">+4%</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-box">
                <div style="font-size: 10px; color: #64748b;">EVALUATIONS</div>
                <div style="font-size: 22px; font-weight: bold; color: #0f172a;">4<span style="font-size: 14px; color: #64748b;">/4</span> <span class="badge-soft-blue">100%</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="peereval-card" style="background-color: #fef3c7; border: 1px solid #fde68a; margin-top: 16px;">
            <div style="font-weight: bold; color: #92400e !important;">⚠️ Score Variance Detected</div>
            <div style="font-size: 12px; color: #b45309 !important;">Statistically significant variance (σ = {health_report['variance']}) observed in technical contribution feedback.</div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("MEMBER DIAGNOSTICS")

    members = [
        {"name": "Marcus Chen", "role": "Lead Architect", "score": "4.8", "status": "Aligned", "badge": "badge-green"},
        {"name": "Elena Rostova", "role": "Distributed Consensus", "score": "4.6", "status": "Aligned", "badge": "badge-green"},
        {"name": "David Kim", "role": "Under-Engagement Flag", "score": "2.3", "status": "-2.1 dev", "badge": "badge-red"},
        {"name": "Priya Patel", "role": "Benchmarking & Testing", "score": "4.4", "status": "Aligned", "badge": "badge-green"},
    ]

    for m in members:
        st.markdown(f"""
            <div class="peereval-card" style="padding: 12px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <b style="color: #0f172a;">{m['name']}</b> <span style="font-size: 11px; color: #64748b;">• {m['role']}</span>
                    </div>
                    <div>
                        <span style="font-weight: bold; font-size: 14px; color: #0f172a;">{m['score']}</span> <span class="{m['badge']}">{m['status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="peereval-card" style="background-color: #e0e7ff; border: none; margin-top: 16px;">
            <div style="font-weight: bold; color: #3730a3 !important; font-size: 12px;">🤖 AUTOMATED INTERVENTION SUGGESTION</div>
            <div style="font-size: 14px; font-weight: bold; color: #1e1b4b !important; margin: 4px 0;">Faculty Sync Recommended</div>
            <div style="font-size: 11px; color: #4338ca !important;">{health_report['recommendation']}</div>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. SCREEN 4: INSTRUCTOR REPORT
# ==========================================
def render_instructor_report(user, group, evaluations: List, health_report: dict):
    inject_custom_css()

    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; color: #0f172a;">PeerEval <span class="badge-purple">DSS Reports</span></h3>
        </div>
        <div class="peereval-card" style="margin-top: 12px;">
            <span style="font-size: 10px; color: #64748b;">ACTIVE COHORT ROSTER</span> <span class="badge-green" style="float: right;">Evaluated (100%)</span>
            <div style="font-weight: bold; font-size: 16px; margin-top: 4px; color: #0f172a;">IS 301 - Section A</div>
            <div style="font-size: 12px; color: #64748b;">42 Students • 9 Project Groups</div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""
        <div class="metric-box">
            <span style="font-size: 10px; color: #64748b;">AVG HEALTH</span>
            <div style="font-size: 18px; font-weight: bold; color: #0f172a;">{int(health_report['avg_score']*20)}%</div>
        </div>
    """, unsafe_allow_html=True)
    c2.markdown("""
        <div class="metric-box">
            <span style="font-size: 10px; color: #64748b;">AT RISK</span>
            <div style="font-size: 18px; font-weight: bold; color: #dc2626;">2</div>
        </div>
    """, unsafe_allow_html=True)
    c3.markdown("""
        <div class="metric-box">
            <span style="font-size: 10px; color: #64748b;">REVIEWS</span>
            <div style="font-size: 18px; font-weight: bold; color: #0f172a;">168</div>
        </div>
    """, unsafe_allow_html=True)

    st.caption("GROUP DIAGNOSTIC TELEMETRY")

    groups = [
        {"code": "GRP-07", "title": "Data Pipeline Architecture", "health": "62%", "var": "±2.3", "flag": "Freeloading Alert", "badge": "badge-red"},
        {"code": "GRP-04", "title": "Distributed Web Systems", "health": "88%", "var": "±1.4", "flag": "Workload Asymmetry", "badge": "badge-soft-blue"},
        {"code": "GRP-01", "title": "Cloud Infrastructure Core", "health": "95%", "var": "±0.2", "flag": "Healthy Synergy", "badge": "badge-green"},
    ]

    for g in groups:
        st.markdown(f"""
            <div class="peereval-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="badge-soft-blue">{g['code']}</span>
                    <span class="{g['badge']}">{g['flag']}</span>
                </div>
                <div style="font-weight: bold; font-size: 14px; margin: 8px 0; color: #0f172a;">{g['title']}</div>
                <div style="display: flex; gap: 16px; font-size: 11px; color: #64748b;">
                    <div>Health: <b style="color: #0f172a;">{g['health']}</b></div>
                    <div>Variance: <b style="color: #0f172a;">{g['var']}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.button("📄 Summary PDF", use_container_width=True)
    with col_btn2:
        st.button("⚡ Export to LMS", use_container_width=True)


# ==========================================
# 5. BOTTOM NAVIGATION BAR
# ==========================================
def render_bottom_nav(current_tab: str) -> str:
    st.markdown("---")
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        btn_eval = st.button("📝 Review", use_container_width=True)
    with nav_col2:
        btn_health = st.button("💚 Health", use_container_width=True)
    with nav_col3:
        btn_reports = st.button("📊 Reports", use_container_width=True)
    with nav_col4:
        btn_account = st.button("👤 Profile", use_container_width=True)

    if btn_eval:
        return "Evaluate"
    elif btn_health:
        return "Health"
    elif btn_reports:
        return "Reports"
    elif btn_account:
        return "Account"
    
    return current_tab
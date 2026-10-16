import streamlit as st
import pandas as pd
import io
import csv
from typing import List, Callable
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 0. INJECT REFINED CUSTOM CSS
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    header[data-testid="stHeader"] { background-color: transparent !important; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 500px !important; margin: 0 auto; }
    .stApp { background-color: #f6f8fe !important; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .peereval-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.06);
        border: 1px solid #eef2ff;
    }
    label, p, span, h1, h2, h3, h4 { color: #1e1b4b !important; font-weight: 500; }
    .badge-purple { background-color: #4f46e5; color: white !important; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .badge-soft-blue { background-color: #e0e7ff; color: #3730a3 !important; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; }
    .badge-green { background-color: #d1fae5; color: #065f46 !important; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }
    .badge-red { background-color: #fee2e2; color: #991b1b !important; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }

    .stButton > button {
        background-color: #4f46e5 !important; color: white !important; border-radius: 10px !important; border: none !important; font-weight: 600 !important; padding: 10px 16px !important;
    }
    .metric-box { background: #ffffff; border-radius: 12px; padding: 12px; border: 1px solid #eef2ff; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
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
    with st.container():
        st.caption("EVALUATION ROLE")
        role_tab = st.radio("Select Role", ["🎓 Student", "📊 Instructor"], horizontal=True, label_visibility="collapsed")
        selected_role = "Student" if "Student" in role_tab else "Instructor"
        user_id = st.text_input("University / Student ID", value="S2024-8921" if selected_role == "Student" else "I2024-101")
        st.text_input("Password or Key", value="password", type="password")
        if st.button("Sign In to Workspace ➔", use_container_width=True):
            on_login_click(selected_role, user_id)


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
            </div>
            <span class="badge-red">⏰ Due in 18h</span>
        </div>
    """, unsafe_allow_html=True)
    st.caption("SELECT PEER TO REVIEW")
    if not other_members:
        st.info("No active teammates available.")
        return
    selected_peer = st.selectbox("Teammate", options=other_members, format_func=lambda x: f"{x.name} ({x.user_id})")
    with st.form("rubric_form"):
        comm = st.slider("💬 Communication & Responsiveness", 1, 5, 5)
        effort = st.slider("💎 Effort & Reliability", 1, 5, 4)
        tech = st.slider("⚙️ Technical Quality", 1, 5, 4)
        feedback = st.text_area("🔒 Confidential Peer Remarks")
        if st.form_submit_button("✈️ Submit Rating", use_container_width=True):
            on_submit_eval(selected_peer.user_id, comm, effort, tech, feedback)
            st.success("Submitted successfully!")


# ==========================================
# 3. SCREEN 3: GROUP HEALTH CHECK
# ==========================================
def render_group_health_view(health_report: dict):
    inject_custom_css()

    st.markdown("""
        <div class="peereval-card" style="background-color: #e0e7ff; border: none;">
            <div style="font-weight: bold; color: #3730a3 !important; font-size: 15px;">💬 EvalBot Health Synthesis <span class="badge-purple">DSS v2.4</span></div>
            <div style="font-size: 12px; color: #4338ca !important; margin-top: 4px;">Peer feedback round complete. Telemetry synchronized.</div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="metric-box">
                <div style="font-size: 10px; color: #64748b;">TEAM HEALTH</div>
                <div style="font-size: 22px; font-weight: bold; color: #0f172a;">{int(health_report['avg_score']*20)}% <span style="font-size: 12px; color: #10b981;">+4%</span></div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="metric-box">
                <div style="font-size: 10px; color: #64748b;">EVALUATIONS</div>
                <div style="font-size: 22px; font-weight: bold; color: #0f172a;">4<span style="font-size: 14px; color: #64748b;">/4</span> <span class="badge-soft-blue">100%</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="peereval-card" style="background-color: #fef3c7; border: 1px solid #fde68a; margin-top: 16px;">
            <div style="font-weight: bold; color: #92400e !important;">⚠️ Score Variance Detected</div>
            <div style="font-size: 12px; color: #b45309 !important;">Statistically significant variance (σ = {health_report.get('sigma', 0.0)}) observed in technical contribution feedback.</div>
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
# 4. SCREEN 4: INSTRUCTOR REPORT & EXPORTS
# ==========================================
def generate_pdf_report(evaluations: List, health_report: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#1e1b4b'), spaceAfter=6)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#64748b'), spaceAfter=15)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#3730a3'), spaceBefore=12, spaceAfter=6)
    
    elements.append(Paragraph("PeerEval DSS - Cohort Summary Report", title_style))
    elements.append(Paragraph("Generated via Automated Institutional Telemetry System", sub_style))
    
    summary_data = [
        ['Metric Category', 'Evaluated Value'],
        ['Average Cohort Health', f"{int(health_report['avg_score']*20)}%"],
        ['Statistical Variance (σ)', f"{health_report.get('sigma', 0.0)}"],
        ['Total Processed Reviews', str(len(evaluations))],
        ['Flagged Risk Status', health_report['status']]
    ]
    t = Table(summary_data, colWidths=[200, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1'))
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("Detailed Evaluation Records", heading_style))
    eval_table_data = [['Eval ID', 'Evaluator', 'Evaluatee', 'Avg Score', 'Feedback']]
    for e in evaluations:
        eval_table_data.append([
            e.eval_id,
            e.evaluator_id,
            e.evaluatee_id,
            str(e.average_score),
            e.feedback[:30] + '...' if len(e.feedback) > 30 else e.feedback
        ])
    
    t_eval = Table(eval_table_data, colWidths=[55, 85, 85, 65, 214])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(t_eval)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

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
    c2.markdown(f"""
        <div class="metric-box">
            <span style="font-size: 10px; color: #64748b;">STATUS</span>
            <div style="font-size: 14px; font-weight: bold; color: #4f46e5;">{health_report['status']}</div>
        </div>
    """, unsafe_allow_html=True)
    c3.markdown(f"""
        <div class="metric-box">
            <span style="font-size: 10px; color: #64748b;">REVIEWS</span>
            <div style="font-size: 18px; font-weight: bold; color: #0f172a;">{len(evaluations)}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        pdf_bytes = generate_pdf_report(evaluations, health_report)
        st.download_button(
            label="📄 Download Summary PDF",
            data=pdf_bytes,
            file_name="PeerEval_Cohort_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with col_btn2:
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['EvalID', 'EvaluatorID', 'EvaluateeID', 'Communication', 'Effort', 'Technical', 'AverageScore', 'Feedback'])
        for e in evaluations:
            writer.writerow([e.eval_id, e.evaluator_id, e.evaluatee_id, e.communication_score, e.effort_score, e.technical_score, e.average_score, e.feedback])
        
        st.download_button(
            label="📊 Export Telemetry CSV",
            data=csv_buffer.getvalue(),
            file_name="PeerEval_Telemetry.csv",
            mime="text/csv",
            use_container_width=True
        )


# ==========================================
# 5. SCREEN 5: UNIFIED PROFILE VIEW
# ==========================================
def render_profile_view(user, group, on_logout_click: Callable):
    inject_custom_css()
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 48px;">👤</div>
            <h2 style="margin: 4px 0 0 0; color: #0f172a !important;">User Account & Session</h2>
            <p style="color: #64748b !important; font-size: 12px; margin-top: 2px;">Manage your institutional identity and access credentials.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="peereval-card">
        <div style="background-color: #f6f8fe; border-radius: 12px; padding: 14px; margin-bottom: 12px; border: 1px solid #eef2ff;">
            <span class="badge-soft-blue" style="float: right;">{user.role}</span>
            <span style="font-size: 10px; color: #64748b !important;">INSTITUTIONAL IDENTITY</span>
            <div style="font-size: 16px; font-weight: bold; color: #1e1b4b !important; margin-top: 2px;">{user.name}</div>
            <div style="font-size: 11px; color: #3730a3 !important;">({user.user_id})</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #eef2ff; border-radius: 12px; padding: 12px; box-shadow: 0 2px 8px rgba(79, 70, 229, 0.04);">
                <span style="font-size: 9px; color: #64748b; font-weight: bold;">ACTIVE COHORT</span>
                <div style="font-size: 13px; font-weight: bold; color: #0f172a; margin-top: 2px;">{group.group_id} A-14</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #eef2ff; border-radius: 12px; padding: 12px; box-shadow: 0 2px 8px rgba(79, 70, 229, 0.04);">
                <span style="font-size: 9px; color: #64748b; font-weight: bold;">SESSION TYPE</span>
                <div style="font-size: 13px; font-weight: bold; color: #0f172a; margin-top: 2px;">Standard SSO</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚪 Standard Secure Logout", use_container_width=True):
        on_logout_click()

    st.markdown("""
        <div style="text-align: center; font-size: 11px; color: #94a3b8 !important; margin-top: 20px;">
            🔒 FERPA Compliant • End-to-End Encrypted Rubrics
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. DYNAMIC ROLE-BASED BOTTOM NAVIGATION BAR
# ==========================================
def render_bottom_nav_for_role(current_tab: str, user_role: str) -> str:
    st.markdown("---")
    
    if user_role == "Instructor":
        # Instructors see Health, Reports, and Profile (Review tab excluded)
        c1, c2, c3 = st.columns(3)
        with c1: b1 = st.button("💚 Health", use_container_width=True, key="nav_health_inst")
        with c2: b2 = st.button("📊 Reports", use_container_width=True, key="nav_reports_inst")
        with c3: b3 = st.button("👤 Profile", use_container_width=True, key="nav_profile_inst")

        if b1: return "Health"
        elif b2: return "Reports"
        elif b3: return "Account"
    else:
        # Students see Review, Health, and Profile (Reports hidden)
        c1, c2, c3 = st.columns(3)
        with c1: b1 = st.button("📝 Review", use_container_width=True, key="nav_eval_stu")
        with c2: b2 = st.button("💚 Health", use_container_width=True, key="nav_health_stu")
        with c3: b3 = st.button("👤 Profile", use_container_width=True, key="nav_profile_stu")

        if b1: return "Evaluate"
        elif b2: return "Health"
        elif b3: return "Account"
        
    return current_tab
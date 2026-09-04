import streamlit as st

import dugaduga_bank_auth as dugaduga_bank_auth
import dugaduga_bank_storage as dugaduga_bank_storage
import dugaduga_bank_transactions as dugaduga_bank_transactions
import dugaduga_bank_analysis as dugaduga_bank_analysis
import dugaduga_bank_utils as dugaduga_bank_utils


# ==========================================
# PAGE CONFIGURATION & BRANDING
# ==========================================

st.set_page_config(
    page_title="DUGADUGA Bank | Secure Digital Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Dark Theme CSS
st.markdown("""
    <style>
    /* Global App & Sidebar Dark Background */
    .stApp, [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
    }

    /* Global Text Color */
    html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #f8f9fa !important;
    }

    /* Sidebar Labels & Radio Buttons */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* Fixed Sidebar Profile Card Styling */
    .sidebar-profile-card {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-left: 4px solid #3b82f6 !important;
        padding: 16px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
    }

    /* Dashboard Virtual Banking Card */
    .banking-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    .banking-card h3 {
        color: #f4d35e !important;
        margin-bottom: 5px;
    }

    /* Input Fields Styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
    }

    /* Buttons Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
    }
    
    /* Metrics Formatting */
    div[data-testid="stMetricValue"] {
        font-weight: 700;
        color: #60a5fa !important;
    }
    
    /* Section Dividers */
    hr {
        border-top: 1px solid #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None


# ==========================================
# LOGIN / REGISTRATION INTERFACE
# ==========================================

if not st.session_state.logged_in:

    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #60a5fa !important; font-size: 2.8rem; margin-bottom: 0;'>🏦 DUGADUGA BANK</h1>
            <p style='color: #94a3b8 !important; font-size: 1.1rem;'>Next-Generation Secure ATM & Online Banking Portal</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        login_tab, register_tab = st.tabs(["🔒 Secure Login", "📝 Open an Account"])

        with login_tab:
            st.markdown("### Access Your Account")
            st.caption("Please enter your account credentials below.")

            st.markdown("**Account Number**")
            account_number = st.text_input("Account Number", key="login_account", placeholder="e.g., 1001", label_visibility="collapsed")

            st.markdown("**4-Digit PIN**")
            pin = st.text_input("PIN", type="password", key="login_pin", placeholder="••••", label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Log In to Portal", use_container_width=True, type="primary"):
                account, message = dugaduga_bank_auth.login_account(account_number, pin)

                if account is not None:
                    st.session_state.logged_in = True
                    st.session_state.account = account
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        with register_tab:
            st.markdown("### Join DUGADUGA Bank")
            st.caption("Fill out the details below to register a new account.")

            st.markdown("**Full Name**")
            name = st.text_input("Full Name", key="register_name", placeholder="Juan Dela Cruz", label_visibility="collapsed")

            st.markdown("**Preferred Account Number**")
            account_number = st.text_input("Preferred Account Number", key="register_account", placeholder="e.g., 1002", label_visibility="collapsed")

            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.markdown("**4-Digit PIN**")
                pin = st.text_input("4-Digit PIN", type="password", key="register_pin", placeholder="••••", label_visibility="collapsed")
            with r_col2:
                st.markdown("**Confirm PIN**")
                confirm_pin = st.text_input("Confirm PIN", type="password", key="register_confirm_pin", placeholder="••••", label_visibility="collapsed")

            st.markdown("**Account Type**")
            account_type = st.selectbox("Account Type", ["Savings Account", "Student Account"], label_visibility="collapsed")

            st.markdown("**Initial Deposit (₱)**")
            starting_balance = st.number_input("Initial Deposit (₱)", min_value=0.0, step=100.0, format="%.2f", label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account Now", use_container_width=True, type="primary"):
                account, message = dugaduga_bank_auth.register_account(
                    name, account_number, pin, confirm_pin, account_type, starting_balance
                )

                if account is not None:
                    st.success(message)
                    st.info("Account created successfully! Switch to Secure Login to enter.")
                else:
                    st.error(message)


# ==========================================
# LOGGED-IN ATM APPLICATION
# ==========================================

else:
    account = st.session_state.account
    is_frozen = getattr(account, "is_frozen", False)

    # --------------------------------------
    # SIDEBAR NAVIGATION & PROFILE CARD
    # --------------------------------------
    with st.sidebar:
        st.markdown("## 🏦 **DUGADUGA BANK**")
        st.caption("Client Banking Portal")
        st.divider()

        st.markdown(f"""
            <div class="sidebar-profile-card">
                <div style="font-weight: bold; font-size: 1.05rem; margin-bottom: 4px; color:#ffffff !important;">
                    {account.account_name}
                </div>
                <div style="font-size: 0.85rem; margin-bottom: 2px; color:#94a3b8 !important;">
                    {account.get_account_type()}
                </div>
                <div style="font-size: 0.85rem; color:#94a3b8 !important;">
                    Acc #: <span style="color: #60a5fa !important; font-weight: bold;">{account.account_number}</span>
                </div>
                <div style="font-size: 0.8rem; margin-top: 6px; color: {'#ef4444' if is_frozen else '#10b981'} !important;">
                    Status: <b>{'FROZEN 🔒' if is_frozen else 'ACTIVE 🟢'}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        menu = st.radio(
            "MAIN MENU",
            [
                "📌 Dashboard",
                "💵 Deposit",
                "🏧 Withdraw",
                "💸 Money Transfer",
                "🏦 Time Deposit Vault",
                "🛡️ Security & PIN",
                "📜 Transaction History",
                "📊 Analytics"
            ]
        )

        st.divider()

        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.account = None
            st.rerun()

    # ======================================
    # DASHBOARD
    # ======================================
    if menu == "📌 Dashboard":
        st.title("Account Dashboard")
        st.write(f"Welcome back, **{account.account_name}**!")

        st.markdown(f"""
            <div class="banking-card">
                <h3>DUGADUGA Direct Banking Card</h3>
                <p style="font-size: 1.2rem; letter-spacing: 2px; color:#cbd5e1 !important;">•••• •••• •••• {account.account_number}</p>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px;">
                    <div>
                        <p style="margin:0; font-size:0.75rem; text-transform: uppercase; color:#94a3b8 !important;">Cardholder</p>
                        <p style="margin:0; font-weight:bold; color:#ffffff !important;">{account.account_name.upper()}</p>
                    </div>
                    <div>
                        <p style="margin:0; font-size:0.75rem; text-transform: uppercase; color:#94a3b8 !important;">Account Type</p>
                        <p style="margin:0; font-weight:bold; color:#ffffff !important;">{account.get_account_type()}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Available Balance", dugaduga_bank_utils.format_currency(account.check_balance()))
        col2.metric("Security Status", "FROZEN 🔒" if is_frozen else "ACTIVE 🟢")
        col3.metric("Account ID", account.account_number)

    # ======================================
    # DEPOSIT
    # ======================================
    elif menu == "💵 Deposit":
        st.title("Deposit Funds")
        c1, c2 = st.columns([2, 1])

        with c1:
            st.markdown(f"**Current Balance:** `{dugaduga_bank_utils.format_currency(account.check_balance())}`")
            st.markdown("**Enter Deposit Amount (₱)**")
            amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f", label_visibility="collapsed")

            if st.button("Confirm Deposit", type="primary", use_container_width=True):
                if not dugaduga_bank_utils.is_valid_amount(amount):
                    st.error("Please enter an amount greater than ₱0.00.")
                else:
                    account.deposit(amount)
                    dugaduga_bank_storage.update_account(account)
                    dugaduga_bank_transactions.record_transaction(account, "Deposit", amount)
                    st.success(f"Deposited {dugaduga_bank_utils.format_currency(amount)} successfully!")
                    st.rerun()

    # ======================================
    # WITHDRAW
    # ======================================
    elif menu == "🏧 Withdraw":
        st.title("Withdraw Cash")
        
        if is_frozen:
            st.error("🚨 Account is currently frozen for security. Withdrawals are disabled.")
        else:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**Available Balance:** `{dugaduga_bank_utils.format_currency(account.check_balance())}`")
                st.markdown("**Enter Withdrawal Amount (₱)**")
                amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f", label_visibility="collapsed")

                if st.button("Confirm Withdrawal", type="primary", use_container_width=True):
                    if not dugaduga_bank_utils.is_valid_amount(amount):
                        st.error("Please enter a valid amount.")
                    elif amount > account.check_balance():
                        st.error("Insufficient balance.")
                    else:
                        account.withdraw(amount)
                        dugaduga_bank_storage.update_account(account)
                        dugaduga_bank_transactions.record_transaction(account, "Withdraw", amount)
                        st.success(f"Withdrew {dugaduga_bank_utils.format_currency(amount)} successfully!")
                        st.rerun()

    # ======================================
    # NEW FEATURE 1: MONEY TRANSFER
    # ======================================
    elif menu == "💸 Money Transfer":
        st.title("Peer-to-Peer Money Transfer")
        st.caption("Send funds instantly to another DUGADUGA Bank account.")

        if is_frozen:
            st.error("🚨 Account is currently frozen. Transfers are disabled.")
        else:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**Available Balance:** `{dugaduga_bank_utils.format_currency(account.check_balance())}`")
                
                st.markdown("**Recipient Account Number**")
                target_acc_no = st.text_input("Target Account Number", placeholder="e.g., 1002", label_visibility="collapsed")
                
                st.markdown("**Transfer Amount (₱)**")
                transfer_amt = st.number_input("Transfer Amount", min_value=0.0, step=50.0, format="%.2f", label_visibility="collapsed")

                if st.button("Execute Transfer", type="primary", use_container_width=True):
                    if target_acc_no == account.account_number:
                        st.error("Cannot transfer funds to your own account.")
                    else:
                        all_accounts = dugaduga_bank_storage.load_accounts()
                        target_account = next((a for a in all_accounts if a.account_number == target_acc_no), None)
                        
                        if not target_account:
                            st.error("Recipient account not found.")
                        elif transfer_amt > account.check_balance():
                            st.error("Insufficient balance for this transfer.")
                        elif transfer_amt <= 0:
                            st.error("Please enter a valid transfer amount.")
                        else:
                            account.withdraw(transfer_amt)
                            target_account.deposit(transfer_amt)
                            
                            dugaduga_bank_storage.update_account(account)
                            dugaduga_bank_storage.update_account(target_account)
                            
                            dugaduga_bank_transactions.record_transaction(account, f"Transfer Out to {target_acc_no}", transfer_amt)
                            dugaduga_bank_transactions.record_transaction(target_account, f"Transfer In from {account.account_number}", transfer_amt)
                            
                            st.success(f"Transferred {dugaduga_bank_utils.format_currency(transfer_amt)} to {target_account.account_name}!")
                            st.rerun()

    # ======================================
    # NEW FEATURE 2: TIME DEPOSIT VAULT
    # ======================================
    elif menu == "🏦 Time Deposit Vault":
        st.title("Fixed Time Deposit Vault")
        st.caption("Lock funds into a high-yield term vault to earn guaranteed interest.")

        st.subheader("Simulate Term Deposit Yield")
        vault_col1, vault_col2 = st.columns(2)
        
        with vault_col1:
            st.markdown("**Lock-in Amount (₱)**")
            principal = st.number_input("Principal Amount", min_value=1000.0, step=500.0, format="%.2f", label_visibility="collapsed")
            
            st.markdown("**Lock Duration**")
            duration = st.selectbox("Select Duration", ["30 Days (3.5% p.a.)", "90 Days (5.0% p.a.)", "180 Days (6.5% p.a.)"], label_visibility="collapsed")

        with vault_col2:
            rate = 0.035 if "30" in duration else (0.050 if "90" in duration else 0.065)
            days = 30 if "30" in duration else (90 if "90" in duration else 180)
            projected_interest = (principal * rate * (days / 365))
            total_yield = principal + projected_interest

            st.metric("Estimated Maturity Value", dugaduga_bank_utils.format_currency(total_yield))
            st.metric("Projected Interest Earned", dugaduga_bank_utils.format_currency(projected_interest))

        st.divider()
        if st.button("Lock Funds into Vault", type="primary", use_container_width=True):
            if principal > account.check_balance():
                st.error("Insufficient available balance to open this vault.")
            else:
                account.withdraw(principal)
                dugaduga_bank_storage.update_account(account)
                dugaduga_bank_transactions.record_transaction(account, f"Time Vault Locked ({days} Days)", principal)
                st.success(f"Vault created! Successfully locked {dugaduga_bank_utils.format_currency(principal)} at {rate*100}% p.a.")
                st.rerun()

    # ======================================
    # NEW FEATURES 3 & 4: SECURITY & EMERGENCY LOCK
    # ======================================
    elif menu == "🛡️ Security & PIN":
        st.title("Security Settings & Shield")
        
        t1, t2 = st.tabs(["🔑 Change PIN", "🚨 Emergency Lock Switch"])

        with t1:
            st.subheader("Update 4-Digit Security PIN")
            st.markdown("**Current PIN**")
            old_p = st.text_input("Current PIN", type="password", key="old_p", label_visibility="collapsed")
            
            st.markdown("**New PIN**")
            new_p = st.text_input("New PIN", type="password", key="new_p", label_visibility="collapsed")
            
            st.markdown("**Confirm New PIN**")
            confirm_p = st.text_input("Confirm New PIN", type="password", key="confirm_p", label_visibility="collapsed")

            if st.button("Update PIN", type="primary"):
                if account._pin != old_p:
                    st.error("Current PIN is incorrect.")
                elif len(new_p) != 4 or not new_p.isdigit():
                    st.error("New PIN must be a 4-digit number.")
                elif new_p != confirm_p:
                    st.error("New PIN and confirmation do not match.")
                else:
                    account._pin = new_p
                    dugaduga_bank_storage.update_account(account)
                    st.success("PIN updated successfully!")

        with t2:
            st.subheader("Emergency Account Shield")
            st.caption("Instantly freeze all withdrawal and transfer capabilities on this account.")
            
            st.warning(f"Current State: **{'FROZEN 🔒' if is_frozen else 'ACTIVE 🟢'}**")
            st.markdown("**Verify Current PIN to Toggle Freeze State**")
            freeze_pin = st.text_input("Verify PIN", type="password", key="frz_pin", label_visibility="collapsed")

            if st.button("Toggle Account Freeze State", type="primary"):
                if account._pin != freeze_pin:
                    st.error("Incorrect PIN authentication.")
                else:
                    account.is_frozen = not getattr(account, "is_frozen", False)
                    dugaduga_bank_storage.update_account(account)
                    status = "FROZEN 🔒" if account.is_frozen else "UNLOCKED 🟢"
                    st.success(f"Account security state changed to {status}.")
                    st.rerun()

    # ======================================
    # TRANSACTION HISTORY & ANALYTICS
    # ======================================
    elif menu == "📜 Transaction History":
        st.title("Transaction History")
        transactions = dugaduga_bank_transactions.get_transactions()
        user_txs = [tx for tx in transactions if tx.get("account_number") == account.account_number]

        if user_txs:
            display_data = [{
                "Date & Time": tx.get("timestamp", "N/A"),
                "Type": tx.get("transaction"),
                "Amount": dugaduga_bank_utils.format_currency(tx.get("amount", 0)),
                "Updated Balance": dugaduga_bank_utils.format_currency(tx.get("balance_after", 0))
            } for tx in user_txs]
            st.dataframe(display_data, use_container_width=True, hide_index=True)
        else:
            st.info("No transaction records found.")

    elif menu == "📊 Analytics":
        st.title("Financial Analytics")
        result = dugaduga_bank_analysis.analyze_transactions(account.account_number)

        st.subheader("1. Activity Overview")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Transactions", result["total_transactions"])
        m2.metric("Total Deposits", result["deposits"])
        m3.metric("Total Withdrawals", result["withdrawals"])

        st.divider()
        st.subheader("2. Cash Flow Breakdown")
        f1, f2, f3 = st.columns(3)
        f1.metric("Total Inflow", dugaduga_bank_utils.format_currency(result["total_deposited"]))
        f2.metric("Total Outflow", dugaduga_bank_utils.format_currency(result["total_withdrawn"]))
        f3.metric("Net Flow", dugaduga_bank_utils.format_currency(result["net_cash_flow"]))

# ######### Learning Signature ######### 
# Programmed by: Adrian Paolo V. Dugaduga
# Date Submitted: September 4, 2026
 
# Program Description: This program is a Streamlit banking application that handles user authentication, deposits, withdrawals, and transaction analysis using OOP concepts.
# Reflection: I learned how to apply Encapsulation, Abstraction, Inheritance, and Polymorphism in Python while connecting an OOP backend to a Streamlit interactive interface.
 
# AI Usage
# [ ] No AI Assistance – Completed independently without AI.
# [/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
# [ ] AI as Collaborative Partner– Used AI to design, structure, or co-create significant code.

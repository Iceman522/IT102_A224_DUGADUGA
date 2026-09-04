import streamlit as st

# TODO 1:# Import the Account class.
from dugaduga_atm_account import Account

# TODO 2:# Import the balance module.
import dugaduga_atm_balance

# TODO 3:# Import the deposit module.
import dugaduga_atm_deposit

# TODO 4:# Import the withdraw module.
import dugaduga_atm_withdraw

# TODO 5:# Import the history module.
import dugaduga_atm_history

# TODO 6:# Import the analysis module.
import dugaduga_atm_analysis


# TODO 7:# Create the Account object.## Account:# Juan Dela Cruz## Starting balance:# ₱10,000.00
account = Account(
    "Juan Dela Cruz",
    10000.00
)


# TODO 8:# Configure the Streamlit page.## Use:# - page title# - page icon# - wide layout
st.set_page_config(
    page_title="Python ATM",
    page_icon="🏦",
    layout="wide"
)


# TODO 9:# Display the main ATM title.
st.title("PYTHON ATM")

# TODO 10:# Display a welcome message# using the account name.
st.write(
    f"Welcome, **{account.account_name}**!"
)

# TODO 11:# Add a divider.
st.divider()


# TODO 12:# Create the sidebar title.
st.sidebar.title("ATM MENU")

# TODO 13:# Create a sidebar radio menu# with the following choices:## - Check Balance# - Deposit# - Withdraw# - View History# - Analyze Transactions
choice = st.sidebar.radio(
    "Select an option:",
    [
        "Check Balance",
        "Deposit",
        "Withdraw",
        "View History",
        "Analyze Transactions"
    ]
)

# TODO 14:# Check whether the selected option# is "Check Balance".
if choice == "Check Balance":

    # TODO 15:# Display a page header.
    st.header("Check Balance")

    # TODO 16:# Call the balance module and# obtain the current account balance.
    balance = dugaduga_atm_balance.check_balance(account)

    # TODO 17:# Display the balance using# a Streamlit metric.
    st.metric("Current Balance", f"₱{balance:,.2f}")

# TODO 18:# Add the "Deposit" branch.
elif choice == "Deposit":

    # TODO 19:# Display the Deposit Money header.
    st.header("Deposit Money")

    # TODO 20:# Create a number input.## Requirements:# - minimum value of 0# - step of 100# - two decimal places
    amount = st.number_input("Enter amount to deposit:", min_value=0.0, step=100.0, format="%.2f")

    # TODO 21:# Create a button named:## Deposit Money
    if st.button("Deposit Money"):

        # TODO 22:# When the button is clicked,# check whether the amount is valid.
        if amount <= 0:
            # TODO 23:# If the amount is invalid,# display a Streamlit error message.
            st.error("Please enter an amount greater than zero.")
        else:
            # TODO 24:# Otherwise, call the deposit module.
            success = dugaduga_atm_deposit.deposit_money(account, amount)

            # TODO 25:# If the deposit is successful,# display a success message.
            if success:
                st.success(f"Successfully deposited ₱{amount:,.2f}!")
                
                # TODO 26:# Display the updated balance# using a Streamlit metric.
                current_balance = dugaduga_atm_balance.check_balance(account)
                st.metric("Updated Balance", f"₱{current_balance:,.2f}")

# TODO 27:# Add the "Withdraw" branch.
elif choice == "Withdraw":

    # TODO 28:# Display the Withdraw Money header.
    st.header("Withdraw Money")

    # TODO 29:# Display the available account balance.
    current_balance = dugaduga_atm_balance.check_balance(account)
    st.write(f"Available Balance: ₱{current_balance:,.2f}")

    # TODO 30:# Create a number input for# the withdrawal amount.
    amount = st.number_input("Enter withdrawal amount:", min_value=0.0, step=100.0, format="%.2f")

    # TODO 31:# Create the Withdraw Money button.
    if st.button("Withdraw Money"):

        # TODO 32:# Check whether the withdrawal# amount is valid.
        # TODO 33:# Display an error if the amount# is zero or negative.
        if amount <= 0:
            st.error("Please enter an amount greater than zero.")

        # TODO 34:# Check whether the requested# amount is greater than the# current balance.
        # TODO 35:# Display an error when the# account has insufficient balance.
        elif amount > current_balance:
            st.error("Insufficient balance.")

        else:
            # TODO 36:# Call the withdrawal module# when the amount is valid.
            success = dugaduga_atm_withdraw.withdraw_money(account, amount)

            # TODO 37:# Display a success message# after a successful withdrawal.
            if success:
                st.success(f"Successfully withdrew ₱{amount:,.2f}!")

                # TODO 38:# Display the updated balance.
                updated_balance = dugaduga_atm_balance.check_balance(account)
                st.metric("Updated Balance", f"₱{updated_balance:,.2f}")
            else:
                st.error("Withdrawal failed. Please try again.")
# TODO 39:# Add the "View History" branch.
elif choice == "View History":

    # TODO 40:# Display the Transaction History header.
    st.header("Transaction History")

    # TODO 41:# Call view_history() from the# history module.
    history_lines = dugaduga_atm_history.view_history()

    # TODO 42:# Create an empty list named# transactions.
    transactions = []

    # TODO 43:# Create an empty dictionary# for the current transaction.
    current_tx = {}

    # TODO 44:# Use a for loop to process# every returned line.
    for line in history_lines:

        # TODO 45:# Remove unnecessary spaces# and newline characters.
        cleaned_line = line.strip()

        # TODO 46:# Skip empty lines.
        if not cleaned_line:
            continue

        # TODO 47:# Detect Timestamp lines.
        if cleaned_line.startswith("Timestamp:"):
            current_tx["Timestamp"] = cleaned_line.replace("Timestamp:", "").strip()

        # TODO 48:# Detect Account lines.
        elif cleaned_line.startswith("Account:"):
            current_tx["Account"] = cleaned_line.replace("Account:", "").strip()

        # TODO 49:# Detect Transaction lines.
        elif cleaned_line.startswith("Transaction:"):
            current_tx["Type"] = cleaned_line.replace("Transaction:", "").strip()

        # TODO 50:# Detect Amount lines.
        elif cleaned_line.startswith("Amount:"):
            current_tx["Amount"] = cleaned_line.replace("Amount:", "").strip()

            # TODO 51:# Add completed transactions# to the transactions list.
            transactions.append(current_tx)
            current_tx = {}

    # TODO 52:# Display the transactions# using an appropriate Streamlit# table component.
    if transactions:
        st.dataframe(transactions, use_container_width=True)

    # TODO 53:# If there are no transactions,# display an informational message.
    else:
        st.info("No transaction history available.")
# TODO 54:# Add the "Analyze Transactions" branch.
elif choice == "Analyze Transactions":

    # TODO 55:# Display the Transaction Analysis header.
    st.header("Transaction Analysis")

    # TODO 56:# Call analyze_transactions()
    analysis = dugaduga_atm_analysis.analyze_transactions()

    # ==========================================
    # TRANSACTION SUMMARY
    # ==========================================
    # TODO 57:# Display:## 1. Transaction Summary
    st.subheader("1. Transaction Summary")

    # TODO 58:# Create three Streamlit columns.
    col1, col2, col3 = st.columns(3)

    # TODO 59:# Display:## Total Transactions
    with col1:
        st.metric("Total Transactions", analysis.get("total_transactions", 0))

    # TODO 60:# Display:## Deposits
    with col2:
        st.metric("Deposits", analysis.get("total_deposits_count", 0))

    # TODO 61:# Display:## Withdrawals
    with col3:
        st.metric("Withdrawals", analysis.get("total_withdrawals_count", 0))

    # ==========================================
    # TRANSACTION AMOUNT ANALYSIS
    # ==========================================
    # TODO 62:# Add a divider.
    st.divider()

    # TODO 63:# Display:## 2. Transaction Amount Analysis
    st.subheader("2. Transaction Amount Analysis")

    # TODO 64:# Create three columns.
    col4, col5, col6 = st.columns(3)

    # TODO 65:# Display:## Total Deposited
    with col4:
        st.metric("Total Deposited", f"₱{analysis.get('total_deposited', 0.0):,.2f}")

    # TODO 66:# Display:## Total Withdrawn
    with col5:
        st.metric("Total Withdrawn", f"₱{analysis.get('total_withdrawn', 0.0):,.2f}")

    # TODO 67:# Display:## Average Transaction
    with col6:
        st.metric("Average Transaction", f"₱{analysis.get('average_transaction', 0.0):,.2f}")

    # ==========================================
    # ACCOUNT ACTIVITY ANALYSIS
    # ==========================================
    # TODO 68:# Add another divider.
    st.divider()

    # TODO 69:# Display:## 3. Account Activity Analysis
    st.subheader("3. Account Activity Analysis")

    # TODO 70:# Create three columns.
    col7, col8, col9 = st.columns(3)

    # TODO 71:# Display:## Latest Transaction
    with col7:
        st.metric("Latest Transaction", analysis.get("latest_transaction_type", "N/A"))

    # TODO 72:# Display:## Largest Transaction
    with col8:
        st.metric("Largest Transaction", f"₱{analysis.get('largest_transaction_amount', 0.0):,.2f}")

    # TODO 73:# Display:## Latest Activity
    with col9:
        st.metric("Latest Activity", analysis.get("latest_activity_time", "N/A"))
# ######### Learning Signature ######### 
# Programmed by: Adrian Paolo V. Dugaduga
# Date Submitted: September 4, 2026
# 
# Program Description: This program serves as the main user interface for the Python ATM system, built with Streamlit to integrate account operations, history viewing, and transaction analysis into a sidebar-driven dashboard.
# Reflection: I learned how to use Streamlit to construct an interactive web interface and connect multiple modular Python scripts into a centralized user experience.
# AI Usage
# [ ] No AI Assistance – Completed independently without AI.
# [/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
# [ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
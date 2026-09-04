from dugaduga_bank_account import (
    SavingsAccount,
    StudentAccount
)
import dugaduga_bank_storage as dugaduga_bank_storage
import dugaduga_bank_utils as dugaduga_bank_utils


def validate_pin(pin):

    if not pin.isdigit():
        return False

    if len(pin) != 4:
        return False

    return True


def register_account(
    name,
    account_number,
    pin,
    confirm_pin,
    account_type,
    starting_balance
):

    name = name.strip()
    account_number = account_number.strip()
    pin = pin.strip()
    confirm_pin = confirm_pin.strip()

    if name == "":
        return None, "Please enter your name."

    if account_number == "":
        return None, "Please enter an account number."

    if dugaduga_bank_storage.account_exists(
        account_number
    ):

        return None, "Account number already exists."

    if not validate_pin(pin):

        return None, (
            "PIN must contain exactly "
            "4 digits."
        )

    if pin != confirm_pin:

        return None, (
            "PIN confirmation does not match."
        )

    if starting_balance < 0:

        return None, (
            "Starting balance cannot be negative."
        )

    if account_type == "Savings Account":

        account = SavingsAccount(
            account_number,
            name,
            pin,
            starting_balance
        )

    else:

        account = StudentAccount(
            account_number,
            name,
            pin,
            starting_balance
        )

    dugaduga_bank_storage.save_account(
        account
    )

    return account, "Registration successful."


def login_account(
    account_number,
    pin
):

    account_number = account_number.strip()
    pin = pin.strip()

    account = (
        dugaduga_bank_storage.find_account(
            account_number
        )
    )

    if account is None:

        return None, (
            "Invalid account number or PIN."
        )

    if not account.verify_pin(pin):

        return None, (
            "Invalid account number or PIN."
        )

    return account, "Login successful."

#Added
def update_pin(account_number, new_pin):
    accounts = dugaduga_bank_storage.load_accounts()
    for acc in accounts:
        if acc.account_number == account_number:
            acc._pin = new_pin
            break
    dugaduga_bank_storage.save_accounts(accounts)

# ######### Learning Signature ######### 
# Programmed by: Adrian Paolo V. Dugaduga
# Date Submitted: September 4, 2026
 
# Program Description: This program manages user authentication, handling login credential verification, PIN updates, and new account registration.
# Reflection: I learned how to validate user inputs, enforce account creation rules, and pass authenticated user data securely to the application.
 
# AI Usage
# [ ] No AI Assistance – Completed independently without AI.
# [/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
# [ ] AI as Collaborative Partner– Used AI to design, structure, or co-create significant code.
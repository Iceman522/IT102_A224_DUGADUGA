# TODO 1:
# Import datetime.
from datetime import datetime
 
# TODO 2:
# Create withdraw_money().
#
# Parameters:
# - account
# - amount
 
 
def withdraw_money(account, amount):
    # TODO 3:
    # Reject zero or negative withdrawal amounts.
    if amount <= 0:
        return False

    # TODO 4:
    # Call the Account object's withdraw()
    # method.
    success = account.withdraw(amount)
 
    # TODO 5:
    # If successful, create a timestamp.
    if success:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
 
    # TODO 6:
    # Open transactions.txt using append mode.
        with open("transactions.txt", "a") as file:
 
    # TODO 7:
    # Write the timestamp.
            file.write(
                f"Timestamp: {timestamp}\n"
            )
 
    # TODO 8:
    # Write the account name.
            file.write(
                f"Account: {account.account_name}\n"
            )
 
    # TODO 9:
    # Write:
    #
    # Transaction: Withdraw
            file.write(
                "Transaction: Withdraw\n"
            )
 
    # TODO 10:
    # Write the withdrawal amount.
            file.write(
                f"Amount: P{amount:.2f}\n\n"
            )
 
    # TODO 11:
    # Return True for a successful withdrawal.
        return True
 
    # TODO 12:
    # Return False when the withdrawal fails.
    return False

""" 
######### Learning Signature ######### 
Programmed by: Adrian Paolo V. Dugaduga
Date Submitted: September 4, 2026
 
Program Description: This program defines a module function that withdraws money from an account object and records the withdrawal details with a timestamp in a text file.
Reflection: I learned how to handle account withdrawals safely and log successful transaction records to a file using append mode.
AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
def analyze_transactions():
    # TODO 1:
    # Try to open transactions.txt.
    #
    # Read all lines from the file.
    try:
        with open("transactions.txt", "r") as file:
            lines = file.readlines()

    # TODO 2:
    # If the file does not exist,
    # return a dictionary containing
    # zero or "None" values for the
    # required analysis results.
    except FileNotFoundError:
        return {
            "total_transactions": 0,
            "deposits": 0,
            "withdrawals": 0,
            "total_deposited": 0,
            "total_withdrawn": 0,
            "average_transaction": 0,
            "latest_transaction": "None",
            "latest_timestamp": "None",
            "largest_transaction": 0
        }

    # TODO 3:
    # Create an empty list named transactions.
    transactions = []

    # TODO 4:
    # Create an empty dictionary named current.
    #
    # This dictionary will temporarily
    # store one transaction.
    current = {}

    # TODO 5:
    # Use a for loop to process every line.
    for line in lines:

        # TODO 6:
        # Remove unnecessary spaces and
        # newline characters.
        line = line.strip()

        # TODO 7:
        # Ignore empty lines.
        if not line:
            continue

        # TODO 8:
        # Detect lines beginning with:
        #
        # Timestamp:
        #
        # Store the timestamp.
        if line.startswith("Timestamp:"):
            current["timestamp"] = (
                line.replace("Timestamp:", "").strip()
            )

        # TODO 9:
        # Detect lines beginning with:
        #
        # Account:
        #
        # Store the account name.
        elif line.startswith("Account:"):
            current["account"] = (
                line.replace("Account:", "").strip()
            )

        # TODO 10:
        # Detect lines beginning with:
        #
        # Transaction:
        #
        # Store the transaction type.
        elif line.startswith("Transaction:"):
            current["type"] = (
                line.replace("Transaction:", "").strip()
            )

        # TODO 11:
        # Detect lines beginning with:
        #
        # Amount:
        #
        # Convert the amount to a float.
        elif line.startswith("Amount:"):
            amount_text = (
                line.replace("Amount:", "")
                .replace("₱", "")
                .replace("P", "")
                .replace(",", "")
                .strip()
            )

            try:
                current["amount"] = float(amount_text)
            except ValueError:
                current["amount"] = 0.0

            # TODO 12:
            # Once the required transaction
            # information has been collected,
            # add the transaction to the
            # transactions list.
            if "type" in current and "amount" in current:
                transactions.append(current.copy())
                current = {}

    # TODO 13:
    # Calculate the total number
    # of transactions.
    total_transactions = len(transactions)

    # TODO 14:
    # Count the number of deposits.
    deposits = 0

    # TODO 15:
    # Count the number of withdrawals.
    withdrawals = 0

    # TODO 16:
    # Calculate the total amount
    # deposited.
    total_deposited = 0

    # TODO 17:
    # Calculate the total amount
    # withdrawn.
    total_withdrawn = 0

    # TODO 18:
    # Determine the largest transaction.
    largest_transaction = 0

    # TODO 19:
    # Determine the latest transaction type.
    latest_transaction = "None"

    # TODO 20:
    # Determine the latest timestamp.
    latest_timestamp = "None"

    for transaction in transactions:
        transaction_type = transaction["type"]
        amount = transaction["amount"]

        if transaction_type == "Deposit":
            deposits += 1
            total_deposited += amount
        elif transaction_type == "Withdraw":
            withdrawals += 1
            total_withdrawn += amount

        if amount > largest_transaction:
            largest_transaction = amount

        latest_transaction = transaction_type

        if "timestamp" in transaction:
            latest_timestamp = transaction["timestamp"]

    # TODO 21:
    # Calculate the average transaction amount.
    #
    # Avoid division by zero.
    if total_transactions > 0:
        total_amount = (
            total_deposited +
            total_withdrawn
        )
        average_transaction = (
            total_amount / total_transactions
        )
    else:
        average_transaction = 0

    # TODO 22:
    # Return all calculated results
    # inside one dictionary.
    return {
        "total_transactions": total_transactions,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "total_deposited": total_deposited,
        "total_withdrawn": total_withdrawn,
        "average_transaction": average_transaction,
        "latest_transaction": latest_transaction,
        "latest_timestamp": latest_timestamp,
        "largest_transaction": largest_transaction
    }

""" 
######### Learning Signature ######### 
Programmed by: Adrian Paolo V. Dugaduga
Date Submitted: September 4, 2026
 
Program Description: This program analyzes transaction logs from a text file to calculate summary statistics like transaction totals, averages, and latest activity.
Reflection: I learned how to to parse structured file data into dictionary objects and perform safe numerical analysis.
AI Usage
[ ] No AI Assistance – Completed independently without AI.
[/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
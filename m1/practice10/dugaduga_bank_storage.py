from dugaduga_bank_account import (
    SavingsAccount,
    StudentAccount
)

USERS_FILE = "users.txt"


def account_exists(account_number):
    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                if line.startswith("Account Number:"):
                    saved_number = (
                        line
                        .replace("Account Number:", "")
                        .strip()
                    )
                    if saved_number == account_number:
                        return True
    except FileNotFoundError:
        return False

    return False


def save_account(account):
    with open(USERS_FILE, "a") as file:
        file.write(
            f"Account Number: {account.account_number}\n"
        )
        file.write(
            f"Account Name: {account.account_name}\n"
        )
        file.write(
            f"PIN: {account.get_pin()}\n"
        )
        file.write(
            f"Account Type: {account.get_account_type()}\n"
        )
        file.write(
            f"Balance: {account.check_balance():.2f}\n\n"
        )


def load_accounts():
    accounts = []

    try:
        with open(USERS_FILE, "r") as file:
            content = file.read().strip()
    except FileNotFoundError:
        return accounts

    if not content:
        return accounts

    # Split into blocks by double newlines to isolate each user record
    blocks = content.split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        current = {}

        for line in lines:
            line = line.strip()
            if line.startswith("Account Number:"):
                current["account_number"] = line.replace("Account Number:", "").strip()
            elif line.startswith("Account Name:"):
                current["account_name"] = line.replace("Account Name:", "").strip()
            elif line.startswith("PIN:"):
                current["pin"] = line.replace("PIN:", "").strip()
            elif line.startswith("Account Type:"):
                current["account_type"] = line.replace("Account Type:", "").strip()
            elif line.startswith("Balance:"):
                try:
                    current["balance"] = float(line.replace("Balance:", "").strip())
                except ValueError:
                    current["balance"] = 0.0

        # Construct instance safely only when all expected keys exist
        required_keys = ("account_number", "account_name", "pin", "account_type", "balance")
        if all(k in current for k in required_keys):
            if current["account_type"] == "Savings Account":
                account = SavingsAccount(
                    current["account_number"],
                    current["account_name"],
                    current["pin"],
                    current["balance"]
                )
            else:
                account = StudentAccount(
                    current["account_number"],
                    current["account_name"],
                    current["pin"],
                    current["balance"]
                )
            accounts.append(account)

    return accounts


def find_account(account_number):
    accounts = load_accounts()

    for account in accounts:
        if account.account_number == account_number:
            return account

    return None


def update_account(account):
    accounts = load_accounts()

    with open(USERS_FILE, "w") as file:
        for saved_account in accounts:
            if saved_account.account_number == account.account_number:
                saved_account._balance = account.check_balance()

            file.write(
                f"Account Number: {saved_account.account_number}\n"
            )
            file.write(
                f"Account Name: {saved_account.account_name}\n"
            )
            file.write(
                f"PIN: {saved_account.get_pin()}\n"
            )
            file.write(
                f"Account Type: {saved_account.get_account_type()}\n"
            )
            file.write(
                f"Balance: {saved_account.check_balance():.2f}\n\n"
            )
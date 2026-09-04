class Account:
    # TODO 1:
    # Create the constructor.
    #
    # It should receive:
    # - name
    # - starting_balance
    #
    # Store the values in appropriate object attributes.

    def __init__(self, name, starting_balance):
        # TODO 2:
        # Store the account name.
        self.account_name = name

        # TODO 3:
        # Store the starting balance as an internal attribute.
        self._balance = starting_balance

    # TODO 4:
    # Create check_balance().
    #
    # This method should return the current
    # account balance.

    def check_balance(self):
        return self._balance

    # TODO 5:
    # Create deposit().
    #
    # If amount is greater than zero:
    # - increase the balance
    # - return True
    #
    # Otherwise:
    # - return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    # TODO 6:
    # Create withdraw().
    #
    # The withdrawal should only be successful when:
    # - amount > 0
    # AND
    # - amount <= current balance
    #
    # If successful:
    # - decrease the balance
    # - return True
    #
    # Otherwise:
    # - do not change the balance
    # - return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        return False

account = Account("Juan Dela Cruz", 10000.00)

# Wrap check_balance() in print() to see the returned value
print("Initial Balance:", account.check_balance())

# Deposit test
account.deposit(1000)
print("Balance after deposit:", account.check_balance())

# Withdraw test (new for Practice 9)
account.withdraw(2000)
print("Balance after withdrawal:", account.check_balance()) 



""" 
######### Learning Signature ######### 
Programmed by: Adrian Paolo V. Dugaduga
Date Submitted: September 4, 2026
 
Program Description: This program defines a bank account class that manages account holder details, tracks balances, and handles deposits and withdrawals.
Reflection: I learned how to create object attributes and implement methods for deposited and withdrawn transactions within a class.
 
AI Usage
[ ] No AI Assistance – Completed independently without AI.
[/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""

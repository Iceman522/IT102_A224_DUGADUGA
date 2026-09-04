# dugaduga_bank_account.py
from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_number, name, pin, starting_balance):
        self.account_number = account_number
        self.account_name = name
        self._pin = pin
        self._balance = starting_balance

    def check_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        return True

    def verify_pin(self, pin):
        return self._pin == pin

    def get_pin(self):
        return self._pin

    @abstractmethod
    def get_account_type(self):
        pass

    @abstractmethod
    def get_withdrawal_limit(self):
        """Returns maximum allowed per single withdrawal transaction."""
        pass


class SavingsAccount(BankAccount):
    def get_account_type(self):
        return "Savings Account"

    def get_withdrawal_limit(self):
        return 50000.0  # Higher transaction limit for regular savings

    # Polymorphic behavior: Savings requires a minimum balance of ₱100
    def withdraw(self, amount):
        if amount > self.get_withdrawal_limit():
            return False
        if (self._balance - amount) < 100.0:
            return False
        return super().withdraw(amount)


class StudentAccount(BankAccount):
    def get_account_type(self):
        return "Student Account"

    def get_withdrawal_limit(self):
        return 10000.0  # Lower transaction limit to prevent student overspending

    # Polymorphic behavior: Student accounts can withdraw down to ₱0 balance
    def withdraw(self, amount):
        if amount > self.get_withdrawal_limit():
            return False
        return super().withdraw(amount)

# Added

def change_pin(self, old_pin: str, new_pin: str, confirm_pin: str) -> tuple[bool, str]:
    if self._pin != old_pin:
        return False, "Current PIN is incorrect."
    if len(new_pin) != 4 or not new_pin.isdigit():
        return False, "New PIN must be a 4-digit number."
    if new_pin != confirm_pin:
        return False, "New PIN and confirmation do not match."
    
    self._pin = new_pin
    return True, "PIN updated successfully!"

def transfer(self, target_account, amount: float) -> tuple[bool, str]:
    if self.is_frozen:
        return False, "Account is frozen. Please unlock to perform transactions."
    if amount <= 0:
        return False, "Transfer amount must be greater than ₱0.00."
    if amount > self._balance:
        return False, "Insufficient balance for transfer."
    
    self.withdraw(amount)
    target_account.deposit(amount)
    return True, f"Successfully transferred ₱{amount:,.2f} to {target_account.account_name}."

def toggle_freeze(self, current_pin: str) -> tuple[bool, str]:
    if self._pin != current_pin:
        return False, "Incorrect PIN authentication."
    
    # Toggle boolean state
    self.is_frozen = not getattr(self, "is_frozen", False)
    status = "FROZEN (Locked)" if self.is_frozen else "ACTIVE (Unlocked)"
    return True, f"Account security status is now {status}."

# ######### Learning Signature ######### 
# Programmed by: Adrian Paolo V. Dugaduga
# Date Submitted: September 4, 2026
 
# Program Description: This program defines the core BankAccount object class to manage account data, balances, deposits, withdrawals, PIN changes, and emergency locks.
# Reflection: I learned how to apply OOP concepts like encapsulation and custom methods to safely update account data.
 
# AI Usage
# [ ] No AI Assistance – Completed independently without AI.
# [/] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
# [ ] AI as Collaborative Partner– Used AI to design, structure, or co-create significant code.
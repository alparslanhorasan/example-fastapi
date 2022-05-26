def add(num1: int, num2: int):
    return num1 + num2

def substract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2

class InsufficientFunds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    # def withdraw(self, amount):
    #     self.balance -= amount

    def withdraw(self, amount):
        if amount > self.balance:
            # raise Exception("Yeterli bakiye yok")
            raise InsufficientFunds("Yeterli bakiye yok")
            # raise ZeroDivisionError()
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1

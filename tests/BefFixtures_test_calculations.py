from app.calculations import add, substract, multiply, divide, BankAccount
import pytest
# def test_add():
#     print("testing....")
#     assert True

# test_add()

# def test_add():
#     print("testing....")
#     sum = add(5,3)
#     assert sum == 8

# def test_add():
#     print("testing....")
#     assert add(5,3) == 8

@pytest.mark.parametrize("num1, num2, expected", [
    (5,3,8),
    (4,3,7),
    (8,4,12)
])
def test_add(num1, num2, expected):
    print("testing....")
    assert add(num1, num2) == expected


def test_substract():
    assert substract(9,4) == 5

def test_multiply():
    assert multiply(4,3) == 12

def test_divide():
    assert divide(20,4) == 5

def test_bank_account_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

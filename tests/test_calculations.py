from app.calculations import add, substract, multiply, divide, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    print("Fixture Method")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

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

def test_bank_account_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    print("Ana Method")
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

# def test_bank_transaction(zero_bank_account):
#     zero_bank_account.deposit(200)
#     zero_bank_account.withdraw(100)
#     assert zero_bank_account.balance == 100

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (50,10,40),
    (1200,1000,200)
])
def test_bank_transaction(zero_bank_account,deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    # with pytest.raises(Exception):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)


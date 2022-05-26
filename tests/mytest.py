from app.calculations import add
# def test_add():
#     print("testing....")
#     assert True

# test_add()

def test_add():
    print("testing....")
    sum = add(5,3)
    assert sum == 8

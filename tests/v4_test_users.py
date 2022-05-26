import pytest
from app import schemas
from.database import client, session

# def test_root(client):
#     response = client.get("/")
#     print(response.json())
#     print(response.json().get('message'))
#     assert response.status_code == 201
#     assert response.json() == {"message": "selami"}
#     assert response.json().get("message") == "selami"
@pytest.fixture
def test_user(client):
    user_data = {"email": "ahorasan@gmail.com", 
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
                     

def test_create_user(client):
    res = client.post("/users/",
                     json = {"email": "hello123@gmail.com", 
                             "password": "password123"})
    # Aşağıda UserOut scheması validation yapıyor
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    # assert res.json().get("email") == "hello123@gmail.com"
    assert res.status_code == 201

# def test_login_user(client,test_user):
#     res = client.post("/login/",
#                      data = {"username": "hello123@gmail.com", 
#                              "password": "password123"})
#     assert res.status_code == 200

def test_login_user(test_user, client):
    res = client.post("/login/",
                     data = {"username": test_user['email'], 
                             "password": test_user['password']})
    assert res.status_code == 200
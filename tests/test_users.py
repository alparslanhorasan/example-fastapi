import pytest
from jose import jwt
from app import schemas
# Aşağıdakine gerek aklmadı. conftest.py kullanıyorum artık
# from.database import client, session
from app.config import settings

# def test_root(client):
#     response = client.get("/")
#     print(response.json())
#     print(response.json().get('message'))
#     assert response.status_code == 201
#     assert response.json() == {"message": "selami"}
#     assert response.json().get("message") == "selami"

# def test_user(client): --> conftest.py'a aktarıldı...


def test_create_user(client):
    res = client.post("/users/",
                      json={"email": "hello123@gmail.com",
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
                      data={"username": test_user['email'],
                            "password": test_user['password']})
    login_res = schemas.Token(**res.json())

    # decode() ile Token içinden payload data'yı çıkartıyor.
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])

    # Buradan payload içindeki 'user_id' yi extract ediyor.
    id = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
# Aşağıdaki değiştitilerek Parametrize edilmiştir.
# def test_incorrect_login(test_user, client):
#     # test_user: to create a test user, client: for requests
#     res = client.post("/login/",
#                       data={"username": test_user['email'],
#                             "password": "wrongPassword"})
#     assert res.status_code == 403
#     assert res.json().get('detail') == 'Invalid Credentials'


@pytest.mark.parametrize("email, password, status_code", [
    ('wronemail@gmail.com', 'password123', 403),
    ('ahorasan@gmail.com', 'wrongpassword', 403),
    ('wronemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('ahorasan@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    # test_user: to create a test user, client: for requests
    res = client.post("/login/",
                      data={"username": email,
                            "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

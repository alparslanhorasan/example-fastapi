

def test_root(client):
    response = client.get("/")
    print(response.json())
    print(response.json().get('message'))
    assert response.status_code == 201
    assert response.json() == {"message": "selami"}
    assert response.json().get("message") == "selami"

def test_create_user(client):
    res = client.post("/users/",
                     json = {"email": "hello123@gmail.com", 
                             "password": "password123"})
    # Aşağıda UserOut scheması validation yapıyor
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    # assert res.json().get("email") == "hello123@gmail.com"
    assert res.status_code == 201
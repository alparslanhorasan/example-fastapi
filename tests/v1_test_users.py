from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base
from app.database import Base
import pytest

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Passw0rd?@localhost/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# We don't need the following: 
# Base = declarative_base()

# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)


# @pytest.fixture
# def Client():
#     # run code before we run our test
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#     # run code before we run our test
#     Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    # run code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


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
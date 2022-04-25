from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

from . import schemas
from .config import settings

# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # Gelen data'yı kopyala
    to_encode = data.copy()
    
    # Bitiş zamanını belirle
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # adding another property to jwt to create the token
    to_encode.update({"exp": expire})
    
    # TOKEN Oluşturulması
    # to_encode: payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# ********************************************************
# Aşağıdaki alan daha aşağıda değiştirilmiştir. **********
# ********************************************************
# Token Verification
# def verify_access_token(token: str, credentials_exception):
#     try:
#         # decode() ile Token içinden payload data'yı çıkartıyor.
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         # Buradan payload içindeki 'user_id' yi extract ediyor.
#         id: str = payload.get('user_id')

#         # print(id) // id geliyor

#         # Payload içinde 'id' yoksa hata, raise exception
#         if id == None:
#             raise credentials_exception

#         # Payload içinde 'id' varsa devam
#         # Validate that token has 'id' in it. 
#         # Aslında bu yukarıda kontrol ediliyor if ile
#         token_data = schemas.TokenData(id=id)
    
#     except JWTError:
#         raise credentials_exception

#     return token_data

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     # print(token)
#     credentials_exception = HTTPException(
#                                 status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail=f"Could not validate credentials",
#                                 headers={"WWW-Autenticate": "Bearer"}
#                                         )
#     # Header'dan gelen 'token' ı varification için gönderiyoruz
#     return verify_access_token(token,credentials_exception)
# ********************************************************
# Buraya kadar                                  **********
# ********************************************************

# Token Verification
def verify_access_token(token: str, credentials_exception):
    try:
        # decode() ile Token içinden payload data'yı çıkartıyor.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Buradan payload içindeki 'user_id' yi extract ediyor.
        id: str = payload.get('user_id')

        # print(id) // id geliyor

        # Payload içinde 'id' yoksa hata, raise exception
        if id == None:
            raise credentials_exception

        # Payload içinde 'id' varsa devam
        # Validate that token has 'id' in it. 
        # Aslında bu yukarıda kontrol ediliyor if ile
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):
    # print(token)
    credentials_exception = HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Could not validate credentials",
                                headers={"WWW-Autenticate": "Bearer"}
                                        )
    # Header'dan gelen 'token' ı varification için gönderiyoruz
    # Bize user_id return ediyor
    token = verify_access_token(token,credentials_exception)

    # print(token) returns Object
    # Bu user_id ile DB'den user'ı getiriyoruz.
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # print(user) returns Object

    # Geriye user döndürüyoruz.
    return user

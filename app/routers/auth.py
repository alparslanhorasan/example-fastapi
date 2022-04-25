from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oath2

router = APIRouter()

# user_credentials: --> gelen verinin schema kontrolü
# db: Session --> DB ile session kuruluması

# Aşağıda OAuth2PasswordRequestForm kullanımı ile yeniden yazıldı
@router.post("/",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # Kullanıcıdan gelen mail'in DB'den bulunarak getirilmesi
    # user_credentials.email --> user_credentials.username
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # Kullanıcı mail'i DB'de yoksa raise exception
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Invalid credentials")
    
    # Kullanıcı DB'de mevcut ise password'leri karşılaştır
    # Mail'ler uyuşmuyorsa raise exception
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Invalid credentials")
    
    # Herşey yolunda

    # Create Token
    access_token = oath2.create_access_token(data={"user_id": user.id})
   
    # return Token
    return {"access_token": access_token, "token_type": "bearer"}
    # return {"Token": "Example Token"}


from sys import prefix
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException,APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

# Create a User in DB
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
 
    # Hash the password user.password
    hashed_password = utils.hash(user.password)
    
    # Modify the Schema with hashed_password
    user.password = hashed_password

    new_user = models.User(**user.dict())
        
    # Bu modeli DB'ye ekle
    db.add(new_user)
    # DB'de Commit et
    db.commit()
    # Son Eklenen Record'ı getir new_user'a
    db.refresh(new_user)

    return new_user


# Get one Record from DB
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id== id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with id: {id} can not be found")
     
    return user

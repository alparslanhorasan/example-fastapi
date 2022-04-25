from fastapi import FastAPI, Depends, Response, status, HTTPException,APIRouter
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()
   

# Getting all data from DB
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
                        current_user: int = Depends(oath2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


# Create a Post in DB
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                            db: Session = Depends(get_db),
                            current_user: int = Depends(oath2.get_current_user)):
    # Eklenecek verileri Model Post'a assign et
    # Aşağıdaki şekilde bir kaç alan varsa OK. Çok alan varsa?
    # new_post = models.Post(
    #      title=post.title, content=post.content, published=post.published
    #  )
    # Aşağıdaki şekilde yukarıdakinin aynısı gerçekleştiriliyor
   
    # print(current_user.email)

    new_post = models.Post(**post.dict())
        
    # Bu modeli DB'ye ekle
    db.add(new_post)
    # DB'de Commit et
    db.commit()
    # Son Eklenen Record'ı getir new_post'a
    db.refresh(new_post)

    return new_post

# Get one Record from DB
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oath2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id== id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
     
    return post



# Delete a Post From DB
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                         current_user: int = Depends(oath2.get_current_user)):
    # Query oluştur.
    post = db.query(models.Post).filter(models.Post.id == id)
    # İlk kayıtı bul getir
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")

    # Delete işlemini gerçekleştir
    # synchronize_session: SQLALchemy Session Basics'den bakabiliriz.
    post.delete(synchronize_session=False)
    
    # DB'de Commit et
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Update a Record in DB
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, 
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oath2.get_current_user)):
    # Query oluştur.
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
    
    # post_query.update({'title': 'Alparslan Horasan', 'content':'Selami Cengiz'},
    #                     synchronize_session=False)
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    # DB'de Commit et
    db.commit()

    return post_query.first()


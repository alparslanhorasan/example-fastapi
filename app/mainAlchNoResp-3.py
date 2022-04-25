from distutils.log import error
from multiprocessing.sharedctypes import synchronized
from turtle import title
from typing import Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from requests import Session
from . import models, schemas
from .database import engine, get_db

app = FastAPI()

# SQLAlchemy için 
models.Base.metadata.create_all(bind=engine)


# pydantic için
class Post(BaseModel):
    title: str
    content:str
    published: bool = True



# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"message": "Hello Alchemy !!!!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # query(models.Post) ifadesi aslında bir SQL ifadesi oluşturuyor.
    # all() ile veriler DB'den çekiliyor.
    # bunu print(db.query(models.Post)) ile görmek mümkün
    return {"data": posts}



# Getting all data from DB
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Create a Post in DB
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Eklenecek verileri Model Post'a assign et
    # Aşağıdaki şekilde bir kaç alan varsa OK. Çok alan varsa?
    # new_post = models.Post(
    #      title=post.title, content=post.content, published=post.published
    #  )
    # Aşağıdaki şekilde yukarıdakinin aynısı gerçekleştiriliyor
    new_post = models.Post(**post.dict())
        
    # Bu modeli DB'ye ekle
    db.add(new_post)
    # DB'de Commit et
    db.commit()
    # Son Eklenen Record'ı getir new_post'a
    db.refresh(new_post)

    return {"New post": new_post}

# Get one Record from DB
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id== id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
     
    return {"post detail": post}



# Delete a Post From DB
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
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

    return {"data": post_query.first()}
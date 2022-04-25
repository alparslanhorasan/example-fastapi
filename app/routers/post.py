from fastapi import FastAPI, Depends, Response, status, HTTPException,APIRouter
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

from sqlalchemy import func

router = APIRouter()
   

# Getting all data from DB
# @router.get("/", response_model=List[schemas.Post])
# JOIN'lu sorgu için 'schemas.PostOut' kulandık 
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                        current_user: int = Depends(oath2.get_current_user),
                        limit: int = 10, 
                        skip: int = 0,
                        search: Optional[str] = ""):
    
    # print(limit)
    # Aşağıdaki sorgu herhangi bir user filtresi uygulamadan 
    # tüm postları getirmektedir.
    # print(models.Post.owner_id)
    # posts = db.query(models.Post).all()

    # 'Limit' kadar post getirilmesi
    # posts = db.query(models.Post).limit(limit).all()

    # Offset kadar atlanarak 'Limit' kadar post getirilmesi
    # posts = db.query(models.Post).limit(limit).offset(skip).all()

    # Search Functionality
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Aşağıdaki sorgu Login olmuş user tarafından yaratılmış 
    # Post'ları getirmektedir
    # Ancak aşağıdaki şekilde uygulamayacağız
    # Onun için aşağıdakini Comment'liyoruz...
    # Yukarıdakini açıyoruz.
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    # Yalın sorgu
    # results = db.query(models.Post)

    # JOIN'lu sorgu. "isouter = True" olmazsa default olarak INNER
    # count var.
    # results = db.query(models.Post, 
    #             func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    #             models.Vote.post_id == models.Post.id, 
    #             isouter = True ).group_by(models.Post.id).all()
   
    # Filtrelerimizi de ekleyelim
    posts = db.query(models.Post, 
                func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                models.Vote.post_id == models.Post.id, 
                isouter = True ).group_by(models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
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
   
    print(current_user.id)
    # owner_id öncesi
    # new_post = models.Post(**post.dict())

    # owner_id'yi ekliyoruz..
    new_post = models.Post(owner_id=current_user.id,**post.dict())
        
    # Bu modeli DB'ye ekle
    db.add(new_post)
    # DB'de Commit et
    db.commit()
    # Son Eklenen Record'ı getir new_post'a
    db.refresh(new_post)

    return new_post

# Get one Record from DB
# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oath2.get_current_user)):

    # Yalın Sorgu
    # post = db.query(models.Post).filter(models.Post.id== id).first()

    # JOIN'lu Sorgu   
    post = db.query(models.Post, 
                func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                models.Vote.post_id == models.Post.id, 
                isouter = True ).group_by(models.Post.id).filter(
                models.Post.id== id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
    
    # Login olan user kendi Post'unu Update edebilmeli
    # Ancak aşağıdaki şekilde uygulamayacağız
    # Onun için aşağıdakini Comment'liyoruz...
    # if post.owner_id != current_user.id: 
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #             detail=f"Not authorized to perform the requested operation")

    return post



# Delete a Post From DB
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                         current_user: int = Depends(oath2.get_current_user)):
    # Query oluştur.
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # İlk kayıtı bul getir
    post = post_query.first()

    # Kayıt yoksa mesaj ver bitir.
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
        
    # Kayıt var demek. Devam...
    # Gelen Kayıt'ın 'owner_id' sini Authentication sonucunu gelen user_id
    # ile karşılaştır.
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Not authorized to perform the requested operation")

    
    # Delete işlemini gerçekleştir
    # synchronize_session: SQLALchemy Session Basics'den bakabiliriz.
    post_query.delete(synchronize_session=False)
    
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

    # İlk Kayıt' getir
    post = post_query.first()
    
    # Kayıt yoksa Hata ve ve Bitir.
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
    
    # Aşağıdaki deneme içindi.
    # post_query.update({'title': 'Alparslan Horasan', 'content':'Selami Cengiz'},
    #                     synchronize_session=False)
    
    # Kayıt var demek. Devam...
    # Gelen Kayıt'ın 'owner_id' sini Authentication sonucunu gelen user_id
    # ile karşılaştır.
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Not authorized to perform the requested operation")
   
    # Update işlemini gerçekleştir.
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    # DB'de Commit et
    db.commit()

    return post_query.first()


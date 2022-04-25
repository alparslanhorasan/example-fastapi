from fastapi import FastAPI, Depends, Response, status, HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oath2

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, 
        db: Session = Depends(database.get_db), 
        current_user: int = Depends(oath2.get_current_user)):
    # vote: schemas.Vote: Body'den gelen verinin validasyonu
    # db: Session = Depends(database.get_db): DB'ye bağlantı
    # current_user: int = Depends(oath2.get_current_user): Login olan
    # User'ın id'si

    # Post DB'de mevcut mu değilmi
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    # Post mevcut değilse
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id {vote.post_id} does not exists")
    # Post mevcutsa devam
    
    # db.query(models.Vote): DB'de "votes" tablosunda sorgu oluştur
    vote_query = db.query(models.Vote).filter(
        # DB'deki post_id ile Body'den gelen post_id eşitse
        models.Vote.post_id == vote.post_id,
        # Ve DB'deki user_id Login olan User'ın user_id'si eşitse
        models.Vote.user_id == current_user.id
    )
    # Böyle bir kayıt'ı ara
    found_vote = vote_query.first()

    # Eğer dir 1 ise (Like ise)
    if vote.dir == 1:
        # İki durum söz konusu
        # Daha önce aynı User O Post için 1 vermişse
        if found_vote:
            # Tekrar 1 vermez. Raise hata...
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} has already voted on Post {vote.post_id}")
        # Daha önce aynı User O Post'a 1 VERMEMİŞSE 
        # Body'den gelen post_id'yi, Login'den olan User'ın id'sini Model'a aktar   
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        # Db'ye ekle
        db.add(new_vote)
        # DB'ye commit et
        db.commit()
        return {"Message":"Successfully added Vote"}
    # dir olarak 0 gönderilmişse
    else:
        # User, Post için bir Vote yapmamışsa Hata Mesajı ver
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Vote does not exists")
        # User, Post için bir Vote YAPMIŞSA
        # Vote'u Db'den sil
        vote_query.delete(synchronize_session=False)
        # DB'de Commit et
        db.commit()
        return {"Message":"Successfully Deleted Vote"}

from distutils.log import error
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# pydantic için
class Post(BaseModel):
    title: str
    content:str
    published: bool = True
    rating: Optional[int] = None

# Bağlanıncaya kadar LOOP
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='Passw0rd?', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successful")
        break
    except Exception as error:
        print("Connecting to DB Failed")
        print("Error", error)
        time.sleep(2)


# Getting all data from DB
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}


# Create a Post in DB
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Aşağıdaki gibi yazmak SQL INJECTION'a açık hale getirdiği için
    # be şekilde yazmıyoruz. Bir alttaki şekilde yazıyoruz.
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #              VALUES (post.title, post.content, post.published) """) 

    cursor.execute("""INSERT INTO posts (title, content, published) 
                                 VALUES (%s, %s, %s) RETURNING * """,
                             (post.title, post.content, post.published)) 
    
    # INSERT işleminden Return olacak veriyi sakla
    new_post = cursor.fetchone()

    # DB'de Commit
    conn.commit()

    return {"New post": new_post}

# Get one Record from DB
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
     
    return {"post detail": post}



# Delete a Post From DB
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    
    deleted_post = cursor.fetchone()
    
    # DB'de Commit
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Update a Record in DB
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, 
                                        content = %s, 
                                        published = %s 
                                        WHERE id = %s
                                        RETURNING * """,
                         (post.title, post.content, post.published,str(id))) 
    
    updated_post = cursor.fetchone()
    
    # DB'de Commit
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")

    return {"data": updated_post}
from distutils.log import error
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()

# pydantic için
class Post(BaseModel):
    title: str
    content:str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "i like pizza", "id": 2}
           ]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "Hello World !!!!"}

# @app.post("/posts")
# def get_posts():
#     # return {"data": "This is your post"}
#     return {"data": my_posts}
    

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     # return {"data": "Succesfully created posts"}
#     return {"New post": f"title: {payload['title']} content: {payload['content']}"}

# Aşağıdaki  bölüm PYDANTIC ile kontrol için
# print edip görelim
# @app.post("/createposts")
# def create_posts(post: Post):
#     #print(post)
#     print(post.title)
#     # return {"data": "Succesfully created posts"}
#     return {"New post": "new data"}

# Pydantic Modelin dictionary'ye çevrilmesi
# @app.post("/createposts") Convention'a uymuyor
# @app.post("/posts")
# def create_posts(post: Post):
#     print(post)
#     # Aşağıda post dictionay'ye çevriliyor
#     print(post.dict())
#     # return {"New post": "new data"}
#     return {"New post": post}

# Aşağıdaki my_posts return ediyor 
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.post("/posts")
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # pydantic modeli dictionay'ye çevirelim
    post_dict = post.dict()
    # "id" alanı ekleyelim. random kullanalım.
    post_dict['id'] = randrange(0,100000)
    # dictionary'mizi "my_posts" arrayine ekleyelim
    my_posts.append(post_dict)
    return {"New post": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # (id: int) bize gelen değerini otomatik olarak int'e çevirir. 
    # (id: str) yaparsak gelen parametreyi str'ye çevirir.   
    # Aşağıdaki iki satırı deneme için kullandık.
    # print(id)
    # return {"post detail": f"Here is post {id}"}
    
    # Şimdi gerçek kodları yazalım:
    # Yukarıdaki 'id' str tipinde. Bunu print(type(id)) gösteriyor.
    # Halbuki 'id' my_posts'da integer. Bu nedenle 
    # aşağıdaki fonksiyonda int'e çevirerek kullanmamız gerekiyor.
    # def get_post(id: int): yazdığımızda aşağıdaki değişir:
    # post = find_post(int(id))
    post = find_post(id)
    # .../posts/asfasf ile çağrıldığında hata döndürür.
    if not post:
        # response.status_code = 404
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")
        # Aşağıdakiler Har Coded. Yukarıda is HTTPExc
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"post with id: {id} can not be found"}
    
    return {"post detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required id
    # my_posts.pop(index) ile ilgili dictionary'yi sil.

    index = find_index_post(id)
    # print(index)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")


    my_posts.pop(index)
    # return {"Message": "post deleted successfully"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)
    # print(index)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} can not be found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
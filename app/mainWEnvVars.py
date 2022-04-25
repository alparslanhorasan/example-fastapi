from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import post, user, auth, item

# Environment Var'ları okuyup valida etmeye yarar 
from pydantic import BaseSettings

# Env. Var.'ları okuyup, validate etmek için önce bir class tanımla
class Settings(BaseSettings):
    # path: int
    # path: str
    #database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key: str = "jjasjdjadjdajdkj"

# Settings class'ı instantiate edilirken Case'lerine bakmadan önce 
# bu değişkenlerin Env. Var. Olarak mevcut olup olmadığına bakar.
# YOKSA; Default değer atanmışsa bu değeri assign eder. Default değer yoksa hata verir.
# VARSA; Bu değeri Validate eder. Gerekirse TYPE CAST eder. Edemezse hata verir.
# Bunların hepsi teker teker denenebilir. 
settings = Settings()

print(settings.database_username)
# SQLAlchemy için 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router, prefix="/posts", tags=['Posts'])
app.include_router(user.router, prefix="/users", tags=['Users'])
app.include_router(auth.router, prefix="/login", tags=['Login'])
app.include_router(item.router, prefix="/items", tags=['Items'])

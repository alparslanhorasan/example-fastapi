from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, item, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# Artık Alembic kullandığımız için aşağıdakilere gerek kalmadı Comment'liyoruz
# # SQLAlchemy için
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# The domains that can talk to our API's
# origins = [
#     "https://www.google.com",
#     "https://www.youtube.com"
# ]
origins = ["*"]

# CORS
# Middleware: A function that runs before other requests
# allow_origins: What domains can talk to our API's
# allow_methods: CORS not only allow domains, it also allows http methods
#                Don't allow POST, PUT methods, allow GET methods like
# allow_headers: Allow only specific headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router, prefix="/posts", tags=['Posts'])
app.include_router(user.router, prefix="/users", tags=['Users'])
app.include_router(auth.router, prefix="/login", tags=['Login'])
app.include_router(item.router, prefix="/items", tags=['Items'])
app.include_router(vote.router, prefix="/votes", tags=['Votes'])

# @app.get("/",status_code=status.HTTP_201_CREATED)


@app.get("/", status_code=status.HTTP_201_CREATED)
def read_root():
    # return {"message": "Bindmount works acaba selami + Cengiz + Halil!!!!"}
    return {"message": "Serap Successfully deployed from CI"}

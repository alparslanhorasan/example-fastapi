# Environment Var'ları okuyup valida etmeye yarar 
from pydantic import BaseSettings

#*************************************************
# Aşağıdakilerin hepsi deneme içindi             *
#*************************************************
# Env. Var.'ları okuyup, validate etmek için önce bir class tanımla
# class Settings(BaseSettings):
#     # path: int
#     # path: str
#     #database_password: str = "localhost"
#     database_username: str = "postgres"
#     secret_key: str = "jjasjdjadjdajdkj"

# Settings class'ı instantiate edilirken Case'lerine bakmadan önce 
# bu değişkenlerin Env. Var. Olarak mevcut olup olmadığına bakar.
# YOKSA; Default değer atanmışsa bu değeri assign eder. Default değer yoksa hata verir.
# VARSA; Bu değeri Validate eder. Gerekirse TYPE CAST eder. Edemezse hata verir.
# Bunların hepsi teker teker denenebilir. 
# settings = Settings()

# print(settings.database_username)

#*************************************************
# Aşağıdakilerin hepsi Gerçek Uygulama için      *
#*************************************************

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

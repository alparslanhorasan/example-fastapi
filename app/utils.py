from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_passord, hashed_password):
    # plain_passord'ü hash'ler ve hashed_password ile karşılatırır.
    # True/False döndürür.
    return pwd_context.verify(plain_passord, hashed_password)
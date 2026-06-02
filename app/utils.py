from passlib.context import CryptContext

# Hashing Algorithm
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto") 

def hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_hash(password: str, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)
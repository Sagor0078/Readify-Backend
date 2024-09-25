

from passlib.context import CryptContext # type: ignore

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str):
    hash = password_context.hash(password)

    return hash

def verify_password(password: str, hash: str) -> bool:
    
    return password_context.verify(password, hash)
    

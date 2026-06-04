from cryptography.fernet import Fernet
from os import getenv

_key = getenv("CRYPTOGRAPHY_KEY")

if not _key:
    raise RuntimeError("cryptography key is not set in enviroment")

fernet = Fernet(_key.encode())

def encrypt(plain:str) -> str:
    return fernet.encrypt(plain.encode()).decode()

def decrypt(token:str) -> str:
    return fernet.decrypt(token.encode()).decode()
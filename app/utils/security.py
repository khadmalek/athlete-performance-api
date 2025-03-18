import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

# Charger les variables d'environnement à partir du fichier .env
load_dotenv("app\.env")

# Récupérer la clé secrète à partir des variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")

# Vérifier si la clé secrète est chargée correctement
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the .env file")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def generate_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)  # Exemple de durée d'expiration
    payload = {
        "sub": username,
        "exp": expiration,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
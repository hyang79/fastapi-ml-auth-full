from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.db import SessionLocal
from app.models import User, RefreshToken
import secrets

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw): return pwd_context.hash(pw)
def verify_password(pw, hpw): return pwd_context.verify(pw, hpw)

def create_token(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data): return create_token(data, timedelta(minutes=15))
def create_refresh_token(data): return create_token(data, timedelta(days=7))

def save_refresh_token(user_id, token):
    db = SessionLocal()
    db_token = RefreshToken(token=token, user_id=user_id)
    db.add(db_token); db.commit(); db.close()

def validate_refresh_token(token):
    db = SessionLocal()
    rec = db.query(RefreshToken).filter_by(token=token).first()
    db.close()
    return rec

def revoke_refresh_token(token):
    db = SessionLocal()
    db.query(RefreshToken).filter_by(token=token).delete()
    db.commit(); db.close()
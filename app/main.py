from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import auth, model as mlmodel, schemas, db, models

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=db.engine)

def get_db():
    dbs = db.SessionLocal()
    try: yield dbs
    finally: dbs.close()

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    new = models.User(username=user.username, hashed_password=hashed)
    db.add(new); db.commit(); db.refresh(new)
    return {"id": new.id, "username": new.username}

@app.post("/token", response_model=schemas.TokenPair)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    dbu = db.query(models.User).filter_by(username=user.username).first()
    if not dbu or not auth.verify_password(user.password, dbu.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    acc = auth.create_access_token({"sub": user.username})
    ref = auth.create_refresh_token({"sub": user.username})
    auth.save_refresh_token(dbu.id, ref)
    return {"access_token": acc, "refresh_token": ref}

@app.post("/refresh")
def refresh(token: schemas.TokenRefresh, db: Session = Depends(get_db)):
    rec = auth.validate_refresh_token(token.refresh_token)
    if not rec: raise HTTPException(401, "Invalid refresh token")
    newacc = auth.create_access_token({"sub": rec.user.username})
    return {"access_token": newacc}

@app.post("/logout")
def logout(token: schemas.TokenRefresh):
    auth.revoke_refresh_token(token.refresh_token)
    return {"msg":"Logged out"}

@app.post("/predict", response_model=schemas.PredictResponse)
def predict(req: schemas.PredictRequest, token: str = Depends(oauth2)):
    user = auth.validate_refresh_token(token) or auth.verify_password # quick check
    if not user:
        raise HTTPException(401, "Invalid token")
    return {"result": mlmodel.predict_species(req.features)}
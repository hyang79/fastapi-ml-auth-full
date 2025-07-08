from pydantic import BaseModel
from typing import List

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(UserRegister):
    pass

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class TokenRefresh(BaseModel):
    refresh_token: str

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    result: int
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets
from passlib.context import CryptContext

class UserBase(BaseModel):
    username: str
    
class User(UserBase):
    password: str
    
class UserInDB(UserBase):
    hashed_pasword: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db: dict[str, UserInDB] = {}

security = HTTPBasic()

def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    found_user = None
    for username, user in fake_users_db.items():
        if secrets.compare_digest(username, credentials.username):
            found_user = user
            break
    if found_user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ivalid credentials",
            headers={"WWW-Authenticate" : "Basic"},
        )
    
    if not pwd_context.verify(credentials.password, found_user.hashed_pasword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenicate": "Basic"},
        )
        
    return found_user

app = FastAPI()

@app.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
        
    hashed = pwd_context.hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_pasword=hashed)
    fake_users_db[user.username] = user_in_db
    
    return {"message": "User registered successfully"}

@app.get("/login")
async def login(current_user: UserInDB = Depends(auth_user)):
    return{"message": f"Welcome, {current_user.username}"}
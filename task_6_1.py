from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

class UserInDatabase(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    username: str
    
USERS_DB: dict[str, UserInDatabase] = {
    "user1": UserInDatabase(
        username="user1",
        password="password1"
    ),
    "user2": UserInDatabase(
        username="user2",
        password="password2"
    ),
}

def get_user_by_username(username: str) -> UserInDatabase | None:
    return USERS_DB.get(username)

security = HTTPBasic()

def raise_unauthorized_error() -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
    
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserOut:
    user = get_user_by_username(credentials.username)
    
    if user is None:
        raise_unauthorized_error()
    if user.password != credentials.password:
        raise_unauthorized_error()
    
    return UserOut(
        username=user.username
    )
    
app = FastAPI()

@app.get("/login")
async def login(current_user: UserOut = Depends(authenticate_user)) -> dict:
    return {
        "message": "You got my secret, welcome!",
        "username": current_user.username
    }
    
 
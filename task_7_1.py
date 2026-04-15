from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import jwt
import datetime
from functools import wraps

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

class User(BaseModel):
    username: str
    roles: List[str]

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

fake_users_db = {
    "admin": {
        "password": "adminpass",
        "roles": ["admin", "user", "guest"]
    },
    "user": {
        "password": "userpass",
        "roles": ["user", "guest"]
    },
    "guest": {
        "password": "guestpass",
        "roles": ["guest"]
    },
}

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_jwt_token(token)
    username = payload.get("sub")
    
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user_data = fake_users_db.get(username)
    if user_data is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(username=username, roles=user_data["roles"])

class PermissionChecker:
    def __init__(self, roles: List[str]):
        self.roles = roles 
    
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Authentication required"
                )
            
            if "admin" in current_user.roles:
                return await func(*args, **kwargs)
            
            if not any(role in current_user.roles for role in self.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper

app = FastAPI()

@app.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    user_data = fake_users_db.get(user.username)
    
    if not user_data or user_data["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_jwt_token({"sub": user.username})
    return TokenResponse(access_token=token)

@app.post("/resources")
@PermissionChecker(["admin"])
async def create_resource(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Resource created by {current_user.username}",
        "role": current_user.roles
    }

@app.delete("/resources/{resource_id}")
@PermissionChecker(["admin"])
async def delete_resource(resource_id: int, current_user: User = Depends(get_current_user)):
    return {
        "message": f"Resource {resource_id} deleted by {current_user.username}",
        "role": current_user.roles
    }

@app.get("/resources")
@PermissionChecker(["user", "admin"])
async def read_resources(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Resources read by {current_user.username}",
        "role": current_user.roles
    }

@app.put("/resources/{resource_id}")
@PermissionChecker(["user", "admin"])
async def update_resource(resource_id: int, current_user: User = Depends(get_current_user)):
    return {
        "message": f"Resource {resource_id} updated by {current_user.username}",
        "role": current_user.roles
    }

@app.get("/public-resources")
@PermissionChecker(["guest", "user", "admin"])
async def read_public_resources(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Public resources read by {current_user.username}",
        "role": current_user.roles
    }

@app.get("/protected_resource")
@PermissionChecker(["admin", "user"])
async def protected_resource(current_user: User = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": current_user.username,
        "role": current_user.roles
    }
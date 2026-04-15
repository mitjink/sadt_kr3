import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "DEV")
DOCS_USER = os.getenv("DOCS_USER", "admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "secret")

security = HTTPBasic()

def protect_docs(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, DOCS_USER)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

if MODE == "PROD":
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
    
    @app.get("/docs", include_in_schema=False)
    @app.get("/openapi.json", include_in_schema=False)
    @app.get("/redoc", include_in_schema=False)
    async def not_found():
        raise HTTPException(status_code=404, detail="Not Found")

elif MODE == "DEV":
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json"
    )
    
    @app.get("/docs", include_in_schema=False, dependencies=[Depends(protect_docs)])
    async def custom_docs():
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=app.openapi_html(), status_code=200)
    
    @app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(protect_docs)])
    async def custom_openapi():
        return app.openapi()

else:
    raise ValueError(f"Unknown MODE: {MODE}. Use DEV or PROD")
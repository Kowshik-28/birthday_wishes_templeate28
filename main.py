from fastapi import FastAPI, Request, status
from models import Base
from Database import engine
from routers import auth, wishes
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.auth import decode_token

app = FastAPI(title="Birthday Wishes Application")

# Create tables in the SQLite database
Base.metadata.create_all(bind=engine)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    token = request.cookies.get('access_token')
    if token:
        user = decode_token(token)
        if user:
            return RedirectResponse(url="/wishes/dashboard", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

@app.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
def chrome_devtools_probe():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Include routers
app.include_router(auth.router)
app.include_router(wishes.router)

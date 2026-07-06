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

# Self-healing database migration for local sqlite upgrades
try:
    import sqlite3
    from Database import default_db_path
    conn = sqlite3.connect(default_db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(wishes)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'video_url' not in columns:
        cursor.execute("ALTER TABLE wishes ADD COLUMN video_url TEXT")
        conn.commit()
        print("Successfully added video_url column to wishes table!")
    conn.close()
except Exception as e:
    print(f"Database self-healing warning: {e}")

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

from typing import Annotated, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status, Form, File, UploadFile
from jose import JWTError
from starlette import status
from models import Wishes, Users
from Database import SessionLocal
from routers.auth import get_current_user, decode_token
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid
import os
import shutil

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/wishes',
    tags=['wishes']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class WishCreateRequest(BaseModel):
    birthday_person_name: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1)
    video_url: Optional[str] = Field(default=None)


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/dashboard")
async def render_dashboard(request: Request, db: db_dependency):
    try:
        token = request.cookies.get('access_token')
        if not token:
            return redirect_to_login()

        user = decode_token(token)
        if user is None:
            return redirect_to_login()

        # Fetch wishes created by this user
        wishes = db.query(Wishes).filter(Wishes.owner_id == user.get("id")).order_by(Wishes.created_at.desc()).all()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"wishes": wishes, "user": user}
        )

    except (JWTError, HTTPException):
        return redirect_to_login()


@router.get("/play/{wish_uuid}")
async def render_play_wish(request: Request, wish_uuid: str, db: db_dependency):
    # Public page - no login required!
    wish = db.query(Wishes).filter(Wishes.wish_uuid == wish_uuid).first()
    if not wish:
        raise HTTPException(status_code=404, detail="Birthday wish not found")

    return templates.TemplateResponse(
        request=request,
        name="play_wish.html",
        context={"wish": wish}
    )


### Endpoints ###

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_wish(
    request: Request, 
    db: db_dependency,
    birthday_person_name: str = Form(...),
    message: str = Form(...),
    video_file: Optional[UploadFile] = File(None)
):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = decode_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    new_uuid = str(uuid.uuid4())
    video_url = None

    if video_file and video_file.filename:
        # Create static/videos directory if it doesn't exist
        videos_dir = os.path.join("static", "videos")
        os.makedirs(videos_dir, exist_ok=True)
        
        # Save file with a unique name based on UUID
        file_ext = os.path.splitext(video_file.filename)[1]
        video_filename = f"{new_uuid}{file_ext}"
        video_path = os.path.join(videos_dir, video_filename)
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
            
        video_url = f"/static/videos/{video_filename}"

    new_wish = Wishes(
        wish_uuid=new_uuid,
        birthday_person_name=birthday_person_name,
        message=message,
        video_url=video_url,
        owner_id=user.get("id")
    )

    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish


@router.delete("/delete/{wish_id}", status_code=status.HTTP_200_OK)
async def delete_wish(request: Request, wish_id: int, db: db_dependency):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = decode_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    wish = db.query(Wishes).filter(Wishes.id == wish_id, Wishes.owner_id == user.get("id")).first()
    if not wish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wish not found or not owned by you")

    # If there is a local video file, delete it
    if wish.video_url and wish.video_url.startswith("/static/videos/"):
        try:
            local_path = wish.video_url.lstrip("/")
            if os.path.exists(local_path):
                os.remove(local_path)
        except Exception as e:
            print(f"Error deleting video file: {e}")

    db.delete(wish)
    db.commit()
    return {"message": "Wish deleted successfully"}

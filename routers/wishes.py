from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from jose import JWTError
from starlette import status
from models import Wishes, Users
from Database import SessionLocal
from routers.auth import get_current_user, decode_token
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid

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
async def create_wish(request: Request, db: db_dependency, wish_req: WishCreateRequest):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = decode_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    new_wish = Wishes(
        wish_uuid=str(uuid.uuid4()),
        birthday_person_name=wish_req.birthday_person_name,
        message=wish_req.message,
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

    db.delete(wish)
    db.commit()
    return {"message": "Wish deleted successfully"}

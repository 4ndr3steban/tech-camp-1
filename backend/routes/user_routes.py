from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import engine
from core.crud import creat_item, read_item, read_user, read_items_by_userid, delete_item
from settings import settings
from config.models import Ttask, Tuser
from schemas.task import Task
from schemas.user import User


router = APIRouter(prefix="/user",
                    tags=["user management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})


crypt = CryptContext(schemes=["bcrypt"])


# Endpoints -------------------------------------------------------------

@router.post("/login", status_code = status.HTTP_202_ACCEPTED)
async def login(form: OAuth2PasswordRequestForm = Depends()):

    try:
        user_db = read_user(Session(engine), form.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": str(user_db.id),
                    "exp": datetime.utcnow() + timedelta(minutes= int(settings.ACCESS_TOKEN_DURATION))}

    return {"access_token": jwt.encode(access_token, settings.SECRET, algorithm=settings.ALGORITHM), "token_type": "bearer"}


@router.post("/register", status_code = status.HTTP_202_ACCEPTED)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    
    try:
        user_db = read_user(Session(engine), user.username)
        if user_db != None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ya existe")
    except:
        pass
    
    hashed_password = crypt.hash(user.password)

    item_id = creat_item(Session(engine), Tuser, User(username=user.username, password=hashed_password))

    access_token = {"sub": str(item_id),
                    "exp": datetime.utcnow() + timedelta(minutes= int(settings.ACCESS_TOKEN_DURATION))}

    return {"access_token": jwt.encode(access_token, settings.SECRET, algorithm=settings.ALGORITHM), "token_type": "bearer"}
# -------------------------------------------------------------
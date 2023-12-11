from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.db import engine
from .crud import read_item
from settings import settings
from config.models import Tuser
from schemas.user import User

oauth2 = OAuth2PasswordBearer(tokenUrl="user/login")

crypt = CryptContext(schemes=["bcrypt"])


async def auth_user(token: str = Depends(oauth2)):
    """ Autentica al usuario desencriptando el token y buscándolo en la base de datos.

    Args:
    - `token` (str): Token de acceso.

    Returns:
    - `User`: Información del usuario autenticado.
    """

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        user_id = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM]).get("sub")
        if user_id is None:
            raise exception

    except JWTError:
        raise exception

    return read_item(Session(engine), Tuser, int(user_id))


async def current_user(user: Tuser = Depends(auth_user)):
    return User(id=user.id, username=user.username)

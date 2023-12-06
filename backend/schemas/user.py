from pydantic import BaseModel

# Clase para manejar los datos de un post como un Schema
class User(BaseModel):
    id: int | None = None
    username: str
    password: str
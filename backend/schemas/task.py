from pydantic import BaseModel

# Clase para manejar los datos de un post como un Schema
class Task(BaseModel):
    id: int | None = None
    fecha_vencimiento: str
    categoria: str
    estado: str | None = "pendiente"
    titulo: str
    descripcion: str | None = None
    info_adic1: str | None = None
    infor_adic2: str | None = None
    id_user: int
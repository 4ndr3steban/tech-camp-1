from pydantic import BaseModel


class Task(BaseModel):
    id: int | None = None
    fecha_vencimiento: str
    periodicidad: str | None = None
    categoria: str
    estado: str | None = "pendiente"
    titulo: str
    descripcion: str | None = None
    info_adic: str | None = None
    id_user: int | None = None
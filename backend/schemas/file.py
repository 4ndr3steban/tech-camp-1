from pydantic import BaseModel


class Filedb(BaseModel):
    id: int | None = None
    content: bytes
    name: str
    content_type: str
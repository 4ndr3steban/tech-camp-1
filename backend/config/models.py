from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, BLOB
from typing import List

# Clase base para los modelos de las tablas para la db
class Base(DeclarativeBase):
    pass


class Ttask(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_vencimiento: Mapped[str] = mapped_column(String(11), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    titulo: Mapped[int] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    info_adic: Mapped[str] = mapped_column(String(255), nullable=True)
    archivo: Mapped[str] = mapped_column(String(255), nullable=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)


class Tuser(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
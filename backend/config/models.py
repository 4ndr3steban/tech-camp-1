from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, CheckConstraint, BLOB
from typing import List

# Clase base para los modelos de las tablas para la db
class Base(DeclarativeBase):
    pass


class Ttask(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_vencimiento: Mapped[str] = mapped_column(String(11), nullable=True)
    periodicidad: Mapped[str] = mapped_column(String(11), nullable=True)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    titulo: Mapped[int] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    info_adic: Mapped[str] = mapped_column(String(255), nullable=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "(periodicidad IS NULL AND fecha_vencimiento IS NOT NULL) OR (periodicidad IS NOT NULL AND fecha_vencimiento IS NULL)", 
            name="check_periodicidad"),
    )


class Tuser(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)


class Tfiles(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(ForeignKey('task.id'), primary_key=True)
    content: Mapped[str] = mapped_column(BLOB, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    content_type = mapped_column(String(100), nullable=False)
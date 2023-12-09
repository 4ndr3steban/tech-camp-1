from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from config.db import engine
from config.models import Tuser, Ttask
from schemas.task import Task
from schemas.user import User


def creat_item(db: Session, table: Tuser | Ttask, item: User | Task):
    """ insertar un elemento en la db

    input: - db: session de conección con la db
           - table: tabla en la cual se va a insetar el dato
           - item: elemento a insertar

    output: id del elemento en la db
    
    """
    # Formatear el item a diccionario
    db_item = item.model_dump()

    # Insertar el item en la db
    res = db.execute(insert(table).values(db_item))

    # Hacer el commit a la db
    db.commit()

    return res.lastrowid


def read_item(db: Session, table: Tuser | Ttask, id: int):
    """ Obtener un item

    input: - db: session de conección con la db
           - table: tabla en la cual se va a insetar el dato
           - id: id del item

    output: item
    
    """
    
    db_query = db.query(table).filter(table.id == id).all()

    return db_query[0]


def read_user(db: Session, username: str):
    """ Obtener un item

    input: - db: session de conección con la db
           - table: tabla en la cual se va a insetar el dato
           - id: id del item

    output: item
    
    """
    
    db_query = db.query(Tuser).filter(Tuser.username == username).all()

    return db_query[0]


def read_items_by_userid(db: Session, id_user: int):
    """ Obtener las tareas de un usuario guardado en la db

    input: - db: session de conección con la db
           - id_user: id del user del que se quieren las tareas

    output: tareas
    
    """
    
    db_query = db.query(Ttask).filter(Ttask.id_user == id_user).all()

    return db_query


def delete_item(db: Session, id: int):
    """ Eliminar un item de la db

    input: - db: session de conección con la db
           - id: id del item que se va a eliminar

    output: 1
    
    """
    
    db.query(Ttask).filter(Ttask.id == id).delete()

    db.commit()

    return 1


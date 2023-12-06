from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from config.db import engine
from config.models import User, Task
from schemas.task import Task
from schemas.user import User


def insert_item(db: Session):
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
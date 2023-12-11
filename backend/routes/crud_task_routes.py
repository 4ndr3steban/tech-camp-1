### API crud para las tareas  ###

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from config.db import engine
from core.crud import creat_item, read_items_by_userid, delete_item
from core.authentication import current_user
from config.models import Ttask
from schemas.task import Task
from schemas.user import User


router = APIRouter(prefix="/task",
                    tags=["task management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})



@router.get("/readtasks", status_code = status.HTTP_202_ACCEPTED)
async def read_task(user: User = Depends(current_user)):
    """ Obtiene las tareas de la base de datos para un usuario específico.

    Args:
    - `user` (User): Token del usuario actual

    Returns:
    - json: objetos JSON que representan las tareas.
    """

    try:
        # Obtener las tareas de la db 
        tasks = read_items_by_userid(Session(engine), user.id)
        return tasks  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las tareas: {str(e)}")  


@router.post("/addtask", status_code = status.HTTP_202_ACCEPTED)
async def add_task(task: Task, user: User = Depends(current_user)):
    """ Agrega una tarea a la base de datos.

    Args:
    - `task` (Task): Datos de la tarea a agregar.
    - `user` (User): Token del usuario actual

    Returns:
    - `item`: id del item agregado a la db
    """
    try:
        # Relacionar el usuario creador de la tarea con la misma
        task.id_user = user.id

        # Agregar la tarea a la db
        item = creat_item(Session(engine), Ttask, task)
        return {"database_item_id": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la tarea: {str(e)}")


@router.put("/updatetask", status_code = status.HTTP_202_ACCEPTED)
async def update_task(task: Task,  user: User = Depends(current_user)):
    """ Actualiza los datos de una tarea en la base de datos.

    Args:
    - `task` (Task): Tarea con los datos a actualizar
    - `user` (User): Token del usuario actual

    Returns:
    - `json`: Un objeto JSON que representa el id de la tarea actualizada.
    """
    try:
        # Obtener la tarea a actualizar
        db = Session(engine)
        task_db = db.query(Ttask).filter(Ttask.id == task.id).first()

        if user.id != task_db.id_user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas para esta tarea",
            headers={"WWW-Authenticate": "Bearer"})
        
        # Setear los nuevos datos a la tarea
        task_db.fecha_vencimiento = task.fecha_vencimiento
        task_db.categoria = task.categoria
        task_db.estado = task.estado
        task_db.titulo = task.titulo
        task_db.descripcion = task.descripcion
        task_db.info_adic = task.info_adic
        task_db.archivo = task.archivo

        # Agregar de nuevo la tarea a la db
        db.add(task_db)
        db.commit()
        
        return {"database_item_id": task_db.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la tarea: {str(e)}")


@router.delete("/deletetask", status_code = status.HTTP_202_ACCEPTED)
async def delete_task(task_id: int, user: User = Depends(current_user)):
    """ Elimina una tarea de la base de datos.

    Args:
    - `task_id` (int): El ID de la tarea que se eliminará
    - `user` (User): Token del usuario actual

    Returns:
    - `Response`: Un objeto JSON con un mensaje que inidca que la tarea se eliminó.
    """

    try:

        # Obtener la tarea a eliminar
        db = Session(engine)
        task_db = db.query(Ttask).filter(Ttask.id == task_id).first()
        
        if not task_db:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarea no encontrada")

        if user.id != task_db.id_user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas para esta tarea",
            headers={"WWW-Authenticate": "Bearer"})
        
        # Eliminar la tarea de la db
        delete_item(Session(engine), task_id)
            
        
        return {"message": "Tarea eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")
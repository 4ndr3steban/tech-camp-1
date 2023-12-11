from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from sqlalchemy.orm import Session
from config.db import engine
from core.crud import creat_item, read_item, read_user, read_items_by_userid, delete_item
from core.authentication import current_user
from settings import settings
from config.models import Ttask
from schemas.task import Task
from schemas.user import User


router = APIRouter(prefix="/task",
                    tags=["task management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})



@router.get("/readtasks", status_code = status.HTTP_202_ACCEPTED)
async def read_task(user: User = Depends(current_user)):

    tasks = read_items_by_userid(Session(engine), user.id)

    return tasks


@router.post("/addtask", status_code = status.HTTP_202_ACCEPTED)
async def add_task(task: Task, user: User = Depends(current_user)):

    task.id_user = user.id
    item = creat_item(Session(engine), Ttask, task)
    return {"database_item_id": item}


@router.put("/updatetask", status_code = status.HTTP_202_ACCEPTED)
async def update_task(task: Task,  user: User = Depends(current_user)):
    
    db = Session(engine)
    task_db = db.query(Ttask).filter(Ttask.id == task.id).first()

    if user.id != task_db.id_user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas para esta tarea",
        headers={"WWW-Authenticate": "Bearer"})

    task_db.fecha_vencimiento = task.fecha_vencimiento
    task_db.categoria = task.categoria
    task_db.estado = task.estado
    task_db.titulo = task.titulo
    task_db.descripcion = task.descripcion
    task_db.info_adic = task.info_adic
    task_db.archivo = task.archivo

    db.add(task_db)
    db.commit()
    
    return {"database_item_id": task_db.id}


@router.delete("/deletetask", status_code = status.HTTP_202_ACCEPTED)
async def delete_task(task_id: int, user: User = Depends(current_user)):
    
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
    
    delete_item(Session(engine), task_id)
        
    
    return {"response": True}
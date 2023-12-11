from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import engine
from core.crud import creat_item, read_item, read_user, read_items_by_userid, delete_item
from core.authentication import current_user
from settings import settings
from config.models import Ttask, Tuser
from schemas.task import Task
from schemas.user import User


router = APIRouter(prefix="/task",
                    tags=["task management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})



@router.get("/statistic", status_code = status.HTTP_202_ACCEPTED)
async def statistics(user: User = Depends(current_user)):

    tasks = read_items_by_userid(Session(engine), user.id)

    today = datetime.now()

    # Obtener el número del día de la semana (lunes es 0 y domingo es 6)
    day_of_week = today.weekday()
    
    # Calcular el primer día de la semana (lunes)
    start_of_week = today - timedelta(days=day_of_week)
    
    # Crear una lista de fechas para toda la semana
    dates_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Convertir las fechas a cadenas en formato "yyyy-mm-dd"
    formatted_dates = [date.strftime("%Y-%m-%d") for date in dates_of_week]
    days_of_week = [date.day for date in dates_of_week]

    def check_period(period: str, days: list):
        hora_periodo = period.split(",")
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        if hora_periodo[1] == "d":
            return True
        elif hora_periodo[1].capitalize() in dias:
            return True
        elif int(hora_periodo[1]) in days:
            return True
        return False

    tasks = list(filter(lambda t: t.fecha_vencimiento in formatted_dates or check_period(t.periodicidad, days_of_week), tasks))

    total_tasks = len(tasks)
    task_cat1 = len(list(filter(lambda t: t.categoria == "trabajo", tasks)))
    task_cat2 = len(list(filter(lambda t: t.categoria == "salud", tasks)))
    task_cat3 = len(list(filter(lambda t: t.categoria == "eventos", tasks)))
    task_cat4 = len(list(filter(lambda t: t.categoria == "academico", tasks)))
    pend_tasks = len(list(filter(lambda t: t.estado == "por hacer", tasks)))
    prog_tasks = len(list(filter(lambda t: t.estado == "en progreso", tasks)))
    fin_tasks = len(list(filter(lambda t: t.estado == "finalizado", tasks)))
    canc_tasks = len(list(filter(lambda t: t.estado == "cancelado", tasks)))

    ans = {
        "total_task_of_week": total_tasks,
        "task_per_category": {"trabajo": task_cat1, "salud": task_cat2, "eventos": task_cat3, "academico": task_cat4},
        "accomplished_tasks": fin_tasks,
        "pending_tasks": pend_tasks,
        "inprogres_tasks": prog_tasks,
        "canceled_tasks": canc_tasks
    }

    return ans



"7:30,12"
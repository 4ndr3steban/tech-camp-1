### Consults statistics API ###

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import engine
from core.crud import read_items_by_userid
from core.authentication import current_user
from schemas.user import User


router = APIRouter(prefix="/task",
                    tags=["task management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})



@router.get("/statistic", status_code = status.HTTP_202_ACCEPTED)
async def statistics(user: User = Depends(current_user)):
    """ Obtiene las estadísticas de tareas realizadas en la semana para un usuario específico.

    Args:
    - `user` (User): Current_user (token de acceso)

    Returns:
    - `ans`: Un objeto JSON que contiene las estadísticas de tareas.
    """
    try:

        # Leer las tareas de la base de datos
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
            """ Checkear cuales de las tareas periodicas se realizan en la semana actual

            Args:
            - `period` (str): atributo 'periodicidad' de una tarea
            - `days` (List): dias de la semana actual ( [10, 11, 12, ...] )

            Returns:
            - `ans`: True o False dependiendo si la tarea se realiza en la semana o no
            
            """

            hora_periodo = period.split(",") if period is not None else ["-1","-1"]
            dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

            if hora_periodo[1] == "d":
                return True
            elif hora_periodo[1].capitalize() in dias:
                return True
            elif int(hora_periodo[1]) in days:
                return True
            return False

        # Filtrar las tareas de la semana
        tasks = list(filter(lambda t: t.fecha_vencimiento in formatted_dates or check_period(t.periodicidad, days_of_week), tasks))

        # Estadisticas
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las estadísticas: {str(e)}")
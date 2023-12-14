from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from config.db import engine
from config.models import Tfiles, Ttask, Tuser
from schemas.task import Task
from schemas.user import User

from app import app

client = TestClient(app)


def test_readtasks():
    # Realizar el login y obtener el token
    login_response = client.post("/user/login", data={"username": "test", "password": "1234"})
    token = login_response.json()["access_token"]

    response = client.get("/task/readtasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 202


def test_addtask():

    # Realizar el login y obtener el token
    login_response = client.post("/user/login", data={"username": "test", "password": "1234"})
    token = login_response.json()["access_token"]

    # Datos de prueba para la tarea
    task_data = {
        "fecha_vencimiento": "test",
        "categoria": "test",
        "estado": "pendiente",
        "titulo": "testT",
        "descripcion": "testD",
        "info_adic": "test"
    }

    # Realiza una solicitud POST al endpoint
    response = client.post("/task/addtask", json=task_data, headers={"Authorization": f"Bearer {token}"})

    # Verifica que la solicitud sea exitosa (código de estado HTTP 200)
    assert response.status_code == 202

    # Verifica que los datos estén almacenados en la base de datos
    db = Session(engine)
    db_task = db.query(Ttask).filter(Ttask.titulo == "testT").first()
    assert db_task is not None
    assert db_task.titulo == "testT"
    assert db_task.descripcion == "testD"
    db.close()


def test_updatetask():

    # Realizar el login y obtener el token
    login_response = client.post("/user/login", data={"username": "test", "password": "1234"})
    token = login_response.json()["access_token"]

    db = Session(engine)

    # Datos de prueba para la actualización de la tarea
    updated_task_data = {
        "id": 1,
        "fecha_vencimiento": "test",
        "categoria": "test",
        "estado": "pendiente",
        "titulo": "Updated Task",
        "descripcion": "This task has been updated",
        "info_adic": "test"
    }

    # Realizar una solicitud PUT al endpoint para actualizar la tarea
    response = client.put(f"/task/updatetask", json=updated_task_data, headers={"Authorization": f"Bearer {token}"})

    # Verificar que la solicitud sea exitosa (código de estado HTTP 200)
    assert response.status_code == 202

    # Verificar que los datos en la base de datos también hayan sido actualizados
    updated_db_task = db.query(Ttask).filter(Ttask.titulo == "Updated Task").first()
    assert updated_db_task.titulo == "Updated Task"
    assert updated_db_task.descripcion == "This task has been updated"
    db.close()


def test_deletetask():

    # Realizar el login y obtener el token
    login_response = client.post("/user/login", data={"username": "test", "password": "1234"})
    token = login_response.json()["access_token"]

    # Añadir una tarea de prueba a la base de datos para eliminar
    db = Session(engine)
    test_task = {
        "fecha_vencimiento": "test",
        "categoria": "test",
        "estado": "pendiente",
        "titulo": "test",
        "descripcion": "test",
        "info_adic": "test",
        "id_user": 1
    }
    db_task = Ttask(**test_task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()

    # Realizar una solicitud DELETE al endpoint para eliminar la tarea
    response = client.delete(f"/task/deletetask?task_id={db_task.id}", headers={"Authorization": f"Bearer {token}"})

    # Verificar que la solicitud sea exitosa (código de estado HTTP 200)
    assert response.status_code == 202

    # Verificar que los datos en la base de datos hayan sido eliminados
    deleted_db_task = db.query(Ttask).filter(Ttask.id == db_task.id).first()
    assert deleted_db_task is None
    db.close()

def test_statistic():
     # Realizar el login y obtener el token
    login_response = client.post("/user/login", data={"username": "test", "password": "1234"})
    token = login_response.json()["access_token"]

    response = client.get("/task/statistic", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 202


def test_login_successful():

    # Realizar una solicitud POST al endpoint para simular un inicio de sesión exitoso
    response = client.post("/user/login", data={"username": "test", "password": "1234"})

    # Verificar que la solicitud sea exitosa (código de estado HTTP 200)
    assert response.status_code == 202

    # Verificar que los datos devueltos sean correctos
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failed():

    # Realizar una solicitud POST al endpoint para simular un inicio de sesión fallido
    response = client.post("/user/login", data={"username": "test", "password": "wrongpassword"})

    # Verificar que la solicitud haya fallado (código de estado HTTP 401)
    assert response.status_code == 400


def test_register_user_successful():

    # Datos de prueba para el registro de usuario
    user_data = {
        "username": "newuser",
        "password": "password123"
    }

    # Realizar una solicitud POST al endpoint para registrar un nuevo usuario
    response = client.post("/user/register", data=user_data)

    # Verificar que la solicitud sea exitosa (código de estado HTTP 200)
    assert response.status_code == 202

    # Verificar que los datos devueltos sean correctos
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_register_user_already_exists():

    # Datos de prueba para el registro de usuario
    user_data = {
        "username": "existinguser",
        "password": "password1234"
    }

    # Registrar al usuario primero
    client.post("/user/register", data=user_data)

    # Intentar registrar al mismo usuario nuevamente
    response = client.post("/user/register", data=user_data)

    # Verificar que la solicitud haya fallado (código de estado HTTP 400)
    assert response.status_code == 400
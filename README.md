# tech-camp-1


### Estructura de directorios
```
└── 📁tech-camp-1
    └── 📁backend
        └── *.env*
        └── app.py
        └── 📁config
            └── db.py
            └── models.py
            └── __init__.py
        └── 📁core
            └── authentication.py
            └── crud.py
            └── mailer.py
            └── __init__.py
        └── requirements.txt
        └── 📁schemas
            └── mailbody.py
            └── task.py
            └── user.py
            └── __init__.py
        └── settings.py
        └── test_app.py
        └── 📁venv
    └── README.md
```

### Inicializar proyecto

* Ubicar una terminal en la carpeta ´Backend´
* En la carpeta ´Backend´ crear un entorno virtual de python con el comando ´python -m venv venv´
* Iniciar el entorno virtual con el comando ´venv\Scripts\activate´ en windows o ´source tutorial-env/bin/activate´ en mac/linux
    * Cambiar el interprete de python por el del entorno virtual si es necesario
* Ejecutar el comando ´pip install -r requirements.txt´
* Crear un archivo con nombre ´.env´ y poner ahí las variables de entorno (mirar la Estructura de directorios)
* Ejecutar el comando ´uvicorn app:app --reload´
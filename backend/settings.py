from dotenv import load_dotenv
from dataclasses import dataclass
import os

# Configuracion de las variables de entorno
@dataclass
class Settings:
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASS: str
    MYSQL_DB: str

# Cargar variables de entorno
load_dotenv()

# Guardar variables de entorno
settings = Settings(MYSQL_HOST = os.getenv("MYSQL_HOST"),
                    MYSQL_USER = os.getenv("MYSQL_USER"),
                    MYSQL_PASS = os.getenv("MYSQL_PASS"),
                    MYSQL_DB = os.getenv("MYSQL_DB"))
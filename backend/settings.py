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
    ALGORITHM: str
    ACCESS_TOKEN_DURATION: int
    SECRET: str
    HOST: str
    MAILUSERNAME: str
    PASSWORD: str
    PORT: str

# Cargar variables de entorno
load_dotenv()

# Guardar variables de entorno
settings = Settings(MYSQL_HOST = os.getenv("MYSQL_HOST"),
                    MYSQL_USER = os.getenv("MYSQL_USER"),
                    MYSQL_PASS = os.getenv("MYSQL_PASS"),
                    MYSQL_DB = os.getenv("MYSQL_DB"),
                    ALGORITHM = os.getenv("ALGORITHM"),
                    ACCESS_TOKEN_DURATION = os.getenv("ACCESS_TOKEN_DURATION"),
                    SECRET = os.getenv("SECRET"),
                    HOST=os.getenv("HOST"),
                    MAILUSERNAME=os.getenv("MAILUSERNAME"),
                    PORT=os.getenv("PORT"),
                    PASSWORD=os.getenv("PASSWORD"))
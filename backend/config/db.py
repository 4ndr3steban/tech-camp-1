from sqlalchemy import Engine, create_engine
from settings import settings
from .models import Base


# Conexión a la base de datos MySql para datos de usuarios y queries
engine = create_engine(f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASS}@localhost:{settings.MYSQL_HOST}/{settings.MYSQL_DB}")

# Metadata para crear las tablas en la db y los tipos de datos en ellas
Base.metadata.create_all(bind=engine)
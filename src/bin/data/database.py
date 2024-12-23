import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

## Obtenemos la conexion a la base de datos con las variabas del entorno.
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

async def get_db_connection():
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    
    
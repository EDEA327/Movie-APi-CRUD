import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_db_name = 'database.sqlite'
# Se lee el directory actual del archivo database.py
base_dir = os.path.dirname(os.path.realpath(__file__))
# Se crea la url de la db
DB_URL = f'sqlite:///{os.path.join(base_dir, sqlite_db_name)}'
# Se crea un motor de db
engine = create_engine(DB_URL, echo=True)
# Inicia una sesión
Session = sessionmaker(bind=engine)
Base = declarative_base()

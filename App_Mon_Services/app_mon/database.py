from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector

SQLALCHAMY_DATABASE_URL = 'mysql+mysqlconnector://root@localhost/app_mon_services'

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password ='',
    database ='app_mon_services'
)
engine = create_engine(SQLALCHAMY_DATABASE_URL)
meta = MetaData()
con = engine.connect()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
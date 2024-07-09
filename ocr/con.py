from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 
from sqlalchemy import create_engine

load_dotenv()

server_name = "ocr-yaya.database.windows.net"
database_name = "ocr-invo"
username = "ocrya"
password = os.getenv("password")
driver = "ODBC Driver 18 for SQL Server"

connection_string = f"mssql+pyodbc://{username}:{password}@{server_name}:1433/{database_name}?driver={driver}"

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)


try:
    conn = engine.connect()
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


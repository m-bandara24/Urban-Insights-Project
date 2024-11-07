import pyodbc
from config import Config

def create_connection():
    conn = pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={Config.SQL_SERVER};DATABASE={Config.DATABASE};UID={Config.USERNAME};PWD={Config.PASSWORD}"
    )
    return conn

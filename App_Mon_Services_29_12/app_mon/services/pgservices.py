import psycopg2
from fastapi import status, HTTPException



def connection(user,password):
    try:
        conn = psycopg2.connect(database="", 
                                user = user, 
                                password = password, 
                                host = "127.0.0.1", 
                                port = "5432")
        cur = conn.cursor() 
        return cur
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"USERNAME OR PASSWORD INCORRECT",headers={"X-Error": "There goes my error"})

  




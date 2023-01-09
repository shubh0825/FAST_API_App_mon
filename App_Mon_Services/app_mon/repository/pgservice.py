from sqlalchemy.orm import Session
import models
from services import pgservices
from fastapi import status, HTTPException

def get_all(id:int,db:Session) :
    try:
        app = db.query(models.App_host.user_name,models.App_host.password).filter(models.App_host.app_host_id == id).first()
        pgservices.connection(app.user_name,app.password)
        print(app.user_name)
        print(app.password)
        return HTTPException(status_code=status.HTTP_200_OK, detail = f"Username and Password Correct")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"USERNAME OR PASSWORD INCORRECT",headers={"X-Error": "There goes my error"})


    
   
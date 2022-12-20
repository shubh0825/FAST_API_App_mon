from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Union
import models, schemas, database
from fastapi import status, HTTPException, Query
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def get_all(db:Session, from_date:Union[str,None] = None , to_date:Union[str,None] = None,query:Union[str,None]=None,\
    offset: int = 0, limit: int = Query(default=100, lte=100)) :
    Q=models.app_mon
    app = db.query(Q)
    rows=app.filter(Q.status =="y").count()
    dt_str =None
    t_str =None
    if from_date:
        try:
            dt_obj = datetime.strptime(from_date,"%Y-%m-%d %H:%M:%S")
            dt_str = datetime.strftime(dt_obj,"%Y-%m-%d %H:%M:%S")
            app = app.filter(Q.date.between(dt_str,datetime.now()))
            rows=app.count()  
        except:
            return HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"Incorrect data format, should be YYYY-MM-DD",headers={"X-Error": "There goes my error"})
    if to_date:
        try:
            to_dt_obj = datetime.strptime(to_date,"%Y-%m-%d %H:%M:%S")
            t_str = datetime.strftime(to_dt_obj,"%Y-%m-%d %H:%M:%S")
            app = app.filter(Q.date <= t_str)
            rows=app.count()  
        except:
            return HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"Incorrect data format, should be YYYY-MM-DD",headers={"X-Error": "There goes my error"})
    if dt_str and t_str: 
        app = app.filter(Q.date.between(dt_str,t_str))
        rows=app.count()    
    if query:
        app = app.filter(or_(Q.app_name.contains(query),(Q.app_key.contains(query))))
        rows=app.count() 
    app=app.filter(Q.status =="y").limit(limit).offset(offset).all()
    return JSONResponse(({'status':'success','error_code': 0,'data':jsonable_encoder(app),'limit':limit,'offset':offset,'total_records':rows,'from_date':from_date,'to_date':to_date}))
        
def create(db:Session,request: schemas.app_mon):
    new_app = models.app_mon(app_name = request.app_name, app_key=request.app_key)
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return JSONResponse(status_code=200, content={"message": "Data Stored Succesfully"})
 
def destroy(id:int,db:Session):
    app = db.query(models.app_mon).filter(models.app_mon.app_id == id)
    if not app.first():
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND,detail = f"App name with id {id} not found",headers={"X-Error": "There goes my error"})
    app.update({models.app_mon.status:"n"})
    db.commit()
    return JSONResponse(content={"MESSAGE":"Remove Data Successfully"})

def update(id:int,db:Session,request: schemas.app_mon):
    app = db.query(models.app_mon).filter(models.app_mon.app_id == id)
    if not app.first():
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND,detail = f"App name with id {id} not found")
    app.update(request.dict())
    db.commit()
    return JSONResponse(content={"MESSAGE":"Data Updated Successfully"},status_code=200)

def show(id:int,db:Session):
    app = db.query(models.app_mon).filter(models.app_mon.app_id == id).first()
    if not app:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND,detail=f'App name with the id {id} is not Available' )
    return app
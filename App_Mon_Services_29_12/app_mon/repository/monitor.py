from sqlalchemy.orm import Session
from typing import Union
import models, schemas
from fastapi import status, HTTPException, Query
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def get_all(db:Session, from_date:Union[str,None] = None , to_date:Union[str,None] = None, offset: int = 0, limit: int = Query(default=100, lte=100)) :
    Q=models.monitoring
    app = db.query(Q)
    rows=app.count()
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
    app=app.limit(limit).offset(offset).all()
    return JSONResponse(({'status':'success','error_code': 0,'data':jsonable_encoder(app),'limit':limit,'offset':offset,'total_records':rows,'from_date':from_date,'to_date':to_date}))
        
def create(db:Session,request: schemas.monitor):
    app = db.query(models.App_host).filter(models.App_host.app_host_id == request.app_host_id)
    if not app.first():
        return JSONResponse(status_code=404, content={"message": "App Host Id not Found"})  
    new_app = models.monitoring(monitor_interval = request.monitor_interval, \
        initial_alert_time=request.initial_alert_time,\
        repeated_alert_time = request.repeated_alert_time,\
        monitor_type_id = request.monitor_type_id,\
        app_host_id = request.app_host_id)
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return JSONResponse(status_code=200, content={"message": "Data Stored Succesfully"})

def destroy(id:int,db:Session):
    app = db.query(models.monitoring).filter(models.monitoring.interval_id== id)
    if not app.first():
        return JSONResponse(content={"MESSAGE":"Monitoring Interval with ID Not Found"},status_code=404)
    app.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(content={"MESSAGE":"Remove Data Successfully"})

def update(id:int,db:Session,request: schemas.monitor):
    app = db.query(models.monitoring).filter(models.monitoring.interval_id == id)
    if not app.first():
        return JSONResponse(content={"MESSAGE":"Monitoring Interval with ID Not Found"},status_code=404)
    app.update(request.dict())
    db.commit()
    return JSONResponse(content={"MESSAGE":"Data Updated Successfully"},status_code=200)

def show(id:int,db:Session):
    app = db.query(models.monitoring).filter(models.monitoring.interval_id == id).first()
    if not app:
        return JSONResponse(content={"MESSAGE":"Monitoring Interval with id not found"},status_code=404)    
    return app
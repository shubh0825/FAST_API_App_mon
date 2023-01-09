from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status, Query
import datetime
from datetime import datetime
from sqlalchemy import or_
from typing import Union
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from ipaddress import ip_address, IPv4Address, IPv6Address

def show(db: Session,from_date:Union[str,None]=None,to_date:Union[str,None]=None,query:Union[str,None]=None,offset: int = 0, limit: int = Query(default=100, lte=100)):
    Q = models.App_host
    apps = db.query(Q)
    dt_str=dt_str1=None
    try:
        if from_date:
            dt_obj = datetime.strptime(from_date,'%Y-%m-%d %H:%M:%S')
            dt_str = datetime.strftime(dt_obj,'%Y-%m-%d %H:%M:%S')
        if to_date:
            dt_obj1 = datetime.strptime(to_date,'%Y-%m-%d %H:%M:%S')
            dt_str1 = datetime.strftime(dt_obj1,'%Y-%m-%d %H:%M:%S')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Date should be in format %Y-%m-%d %H:%M:%S')
    if query:
            apps=apps.filter(or_(Q.app_host_name.contains(query),(Q.user_name.contains(query))))
    if dt_str and dt_str1:
            apps = apps.filter(Q.date.between(dt_str,dt_str1))
    rows = apps.count()
    if dt_str:
        apps = apps.filter(Q.date.between(dt_str,datetime.now()))
    rows = apps.count()
    if dt_str1:
        apps = apps.filter(Q.date <= dt_str1)
    rows = apps.count()
    rows = apps.filter(Q.status == "y").count()
    apps=apps.filter(Q.status =="y").limit(limit).offset(offset).all()
    return JSONResponse({'status':'success','error_code': 0,'total records':rows, 'data':jsonable_encoder(apps),'from_date':dt_str,'to_date':dt_str1,'limit':limit,'offset':offset})

def showapp(id: int,db:Session):
    app = db.query(models.App_host).filter(models.App_host.app_id == id).first()
    if not app:
         return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f'App with id {id} not available',
        )
    return app

def create(request: schemas.App_host, db: Session):
    app = db.query(models.app_mon).filter(models.app_mon.app_id == request.app_id)
    if not app.first():
        return JSONResponse(status_code=500,content={"message": "App not found for this app_id"} )
    try:
            if type(ip_address(request.ip)) is IPv4Address or type(ip_address(request.ip)) is IPv6Address:
                new_app = models.App_host(app_id=request.app_id,app_host_name=request.app_host_name,project_id=request.project_id,ip=request.ip,port=request.port,cred_req=request.cred_req,user_name=request.user_name,password=request.password,app_req_url=request.app_req_url,app_instance=request.app_instance,service_status=request.service_status,service_status_details=request.service_status_details,monitor_method=request.monitor_method,probe_id=request.probe_id,maintenance_mode=request.maintenance_mode,status=request.status)
                db.add(new_app)
                db.commit()
                db.refresh(new_app)
                return JSONResponse(status_code=201, content={"message": "Application details stored successfully"})
    except:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"IP adress should be IPV4 or IPV6",headers={"X-Error": "There goes my error"})  

def update(id:int,request: schemas.App_host,db: Session):
    app = db.query(models.App_host).filter(models.App_host.app_host_id == id)
    if not app.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'app with id {id} not found')
    app1 = db.query(models.app_mon).filter(models.app_mon.app_id == request.app_id)
    if not app1.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'app id is not found')
 
    app.update(request.dict())
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Application details updated successfully"})

def delete(id:int, db: Session):
    app = db.query(models.App_host).filter(models.App_host.app_host_id ==id)
    if not app.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'App with id {id} not found')
    app.update({models.App_host.status:"n"})
    db.commit()
    return 'done'
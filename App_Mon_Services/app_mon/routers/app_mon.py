from fastapi import APIRouter
from typing import Union
from fastapi import Depends, status
import models, schemas, database
from sqlalchemy.orm import Session
from repository import app_mon
from fastapi import Query


router = APIRouter(
    tags=['appmon'],
    prefix = "/appmon",
)
  
@router.get('/')
def all(from_date:Union[str,None]=None, to_date : Union[str,None]=None,db: Session = Depends(database.get_db),query:Union[str,None]=None,\
    offset: int = 0, limit: int = Query(default=100, lte=100)):
    return app_mon.get_all(db,from_date,to_date,query,offset,limit)


@router.post('/',status_code = status.HTTP_201_CREATED)
def create(request: schemas.app_mon, db: Session = Depends(database.get_db)):
    return app_mon.create(db,request)

@router.delete('/{id}',status_code = status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session = Depends(database.get_db)):
    return app_mon.destroy(id,db)

@router.get('/{id}',status_code=200, response_model= schemas.ShowApp)
def show(id:int,db: Session = Depends(database.get_db)):
    return app_mon.show(id,db)

@router.put('/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.app_mon, db: Session = Depends(database.get_db)):
    return app_mon.update(id,db,request)

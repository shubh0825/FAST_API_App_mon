from fastapi import APIRouter
from typing import Union
from fastapi import Depends, status
import schemas, database
from sqlalchemy.orm import Session
from repository import monitor
from fastapi import Query

router = APIRouter(
    tags=['Monitoring Services'],
    prefix = "/App_Monitor",
)

@router.get('/')
def all(from_date:Union[str,None]=None, to_date : Union[str,None]=None, db: Session = Depends(database.get_db), offset: int = 0, limit: int = Query(default=100, lte=100)):
    return monitor.get_all(db,from_date,to_date,offset,limit)

@router.post('/',status_code = status.HTTP_201_CREATED)
def create(request: schemas.monitor, db: Session = Depends(database.get_db)):
    return monitor.create(db,request)

@router.delete('/{id}',status_code = status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session = Depends(database.get_db)):
    return monitor.destroy(id,db)

@router.get('/{id}',status_code=200, response_model= schemas.ShowMon)
def show(id:int,db: Session = Depends(database.get_db)):
    return monitor.show(id,db)

@router.get('/')
def show(id:int,db: Session = Depends(database.get_db)):
    return monitor.pgservices(id,db)

@router.put('/{id}',status_code = status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.monitor, db: Session = Depends(database.get_db)):
    return monitor.update(id,db,request)


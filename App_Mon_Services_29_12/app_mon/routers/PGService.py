from fastapi import APIRouter
from fastapi import Depends
import database
from sqlalchemy.orm import Session
from repository import pgservice



router = APIRouter(
    tags=['PG Services'],
    prefix = "/PG",
)

@router.get('/')
def all(id:int,db: Session = Depends(database.get_db)):
    return pgservice.get_all(id,db)
    
 

# @router.post('/',status_code = status.HTTP_201_CREATED)
# def create(request: schemas.monitor, db: Session = Depends(database.get_db)):
#     return monitor.create(db,request)

# @router.delete('/{id}',status_code = status.HTTP_204_NO_CONTENT)
# def destroy(id:int,db: Session = Depends(database.get_db)):
#     return monitor.destroy(id,db)

# @router.get('/{id}',status_code=200, response_model= schemas.ShowMon)
# def show(id:int,db: Session = Depends(database.get_db)):
#     return monitor.show(id,db)

# @router.get('/')
# def show(id:int,db: Session = Depends(database.get_db)):
#     return monitor.pgservices(id,db)

# @router.put('/{id}',status_code = status.HTTP_202_ACCEPTED)
# def update(id:int,request: schemas.monitor, db: Session = Depends(database.get_db)):
#     return monitor.update(id,db,request)


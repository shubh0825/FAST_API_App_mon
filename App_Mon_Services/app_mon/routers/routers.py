from fastapi import APIRouter
import database, schemas, oauth2, models, token_2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,status,HTTPException
from repository import user, app_mon, monitor, pgservice,app_host
from typing import Union
from fastapi import Query
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash

router = APIRouter()
#-----------------------------------------------User------------------------------------------------------

@router.post('/user', tags=['user'], response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)

@router.get('/user/{id}',tags=['user'], response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(database.get_db)):
    return user.show(id, db)

#----------------------------App Monitoring Services-----------------------------------------------

@router.get('/app_mon',tags=['app-mon-services'])
def all(from_date:Union[str,None]=None, to_date : Union[str,None]=None,db: Session = Depends(database.get_db),query:Union[str,None]=None,\
    offset: int = 0, limit: int = Query(default=100, lte=100)):
    return app_mon.get_all(db,from_date,to_date,query,offset,limit)

@router.post('/app_mon',tags=['app-mon-services'],status_code = status.HTTP_201_CREATED)
def create(request: schemas.app_mon, db: Session = Depends(database.get_db)):
    return app_mon.create(db,request)

@router.delete('/app_mon/{id}',tags=['app-mon-services'],status_code = status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session = Depends(database.get_db)):
    return app_mon.destroy(id,db)

@router.get('/app_mon/{id}',tags=['app-mon-services'],status_code=200, response_model= schemas.ShowApp)
def show(id:int,db: Session = Depends(database.get_db)):
    return app_mon.show(id,db)

@router.put('/app_mon/{id}',tags=['app-mon-services'],status_code = status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.app_mon, db: Session = Depends(database.get_db)):
    return app_mon.update(id,db,request)

#------------------------------------ Monitoring -----------------------------------------------------------------------

@router.get('/App_Monitor',tags=['monitoring'])
def all(from_date:Union[str,None]=None, to_date : Union[str,None]=None, db: Session = Depends(database.get_db), offset: int = 0, limit: int = Query(default=100, lte=100), \
    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return monitor.get_all(db,from_date,to_date,offset,limit)

@router.post('/App_Monitor',tags=['monitoring'],status_code = status.HTTP_201_CREATED)
def create(request: schemas.monitor, db: Session = Depends(database.get_db),\
    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return monitor.create(db,request)

@router.delete('/App_Monitor/{id}',tags=['monitoring'],status_code = status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session = Depends(database.get_db)):
    return monitor.destroy(id,db)

@router.get('/App_Monitor/{id}',tags=['monitoring'],status_code=200, response_model= schemas.ShowMon)
def show(id:int,db: Session = Depends(database.get_db),\
    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return monitor.show(id,db)

@router.put('/App_Monitor/{id}',tags=['monitoring'],status_code = status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.monitor, db: Session = Depends(database.get_db)):
    return monitor.update(id,db,request)

#-----------------------------------------App Host ---------------------------------------------------------
@router.get('/app_host',tags=['app host'])
def show(from_date:Union[str,None]=None,to_date:Union[str,None]=None,query:Union[str,None]=None,offset: int = 0, limit: int = Query(default=100, lte=100),db: Session = Depends(database.get_db)):
    return app_host.show(db,from_date,to_date,query,offset,limit)

@router.get('/app_host/{id}', tags=['app host'],status_code = 200, response_model=schemas.Showapphost)
def showapp(id:int,db: Session = Depends(database.get_db)):
    return app_host.showapp(id,db)

@router.post('/app_host',tags=['app host'], status_code= status.HTTP_201_CREATED)
def create(request: schemas.App_host,current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    return app_host.create(request, db)

@router.put('/app_host/{id}',tags=['app host'],status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.App_host,current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    return app_host.update(id, request,db)

@router.delete('/app_host/{id}',tags=['app host'],status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, current_user: schemas.User = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db)):
    return app_host.delete(id, db)

#--------------------------------------PG Services -----------------------------------------------------------

@router.get('/pg',tags=['pg_services'])
def all(id:int,db: Session = Depends(database.get_db)):
    return pgservice.get_all(id,db)

#--------------------------------------- Authentication----------------------------------------------------

@router.post('/login',tags=['authentication'])
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    User = db.query(models.User).filter(models.User.email == request.username).first()
    if not User:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")
    if not Hash.verify(User.password,request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Incorrect Password..")
    access_token = token_2.create_access_token(data={"sub": User.email})
    return {"access_token": access_token, "token_type": "bearer"}
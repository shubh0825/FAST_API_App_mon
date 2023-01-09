from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from hashing import Hash



def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    if not (len(new_user.name) >=3 and len(new_user.name) <=5):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Username...Enter the Username in between 3 to 5 Char")
    elif not new_user.name.isalpha():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Enter Valid Username in CHar Format...")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
from sqlalchemy import Column, Integer, String,Enum, DateTime
from database import Base
from sqlalchemy.sql import func
import enum

class Status(enum.Enum):
    y = "y"
    n = "n"
   
class app_mon(Base):
    __tablename__ = 'app_master'
    app_id = Column(Integer, primary_key=True)
    app_name = Column(String(255), nullable =True)
    app_key = Column(String(255), nullable = True)
    status=  Column(Enum(Status),nullable=False,default=Status.y)
    date_modified = Column(DateTime(timezone = True), onupdate = func.now(), server_default=func.now())
    date = Column(DateTime(timezone = True), server_default=func.now())
   

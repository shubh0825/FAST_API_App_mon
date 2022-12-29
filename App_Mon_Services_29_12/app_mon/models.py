from sqlalchemy import Column, Integer, String,Enum, DateTime, VARCHAR,BigInteger, Text, ForeignKey
from database import Base
from sqlalchemy.sql import func
import enum

class Status(enum.Enum):
    y = "y"
    n = "n"
   
class Cred(enum.Enum):
    y = "y"
    n = "n"

class Service(enum.Enum):
    y = "y"
    n = "n"

class Maintenance(enum.Enum):
    y = "y"
    n = "n"

class app_mon(Base):
    __tablename__ = 'app_master1'
    app_id = Column(Integer, primary_key=True)
    app_name = Column(String(255), nullable =True)
    app_key = Column(String(255), nullable = True)
    status=  Column(Enum(Status),nullable=False,default=Status.y)
    date_modified = Column(DateTime(timezone = True), onupdate = func.now(), server_default=func.now())
    date = Column(DateTime(timezone = True), server_default=func.now())
    monitor_interval = Column(Integer, nullable= True)
    initial_alert_time = Column(Integer, nullable =True)
    repeated_alert_time = Column(Integer, nullable =True)

class App_host(Base):
    __tablename__='app_host'
    app_host_id = Column(Integer,primary_key=True)
    app_id = Column(Integer, ForeignKey('app_master1.app_id'))
    app_host_name = Column(VARCHAR(255),nullable=True)
    project_id = Column(VARCHAR(50))
    ip = Column(VARCHAR(50),nullable=True)
    port = Column(Integer,nullable=True)
    cred_req = Column(Enum(Cred),default=Cred.y)
    user_name = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    app_req_url = Column(Text,nullable=True)
    app_instance = Column(VARCHAR(255),nullable=True)
    service_status = Column(Enum(Service), default=Service.y)
    service_status_details = Column(Text,nullable=True)
    monitor_method = Column(VARCHAR(255),nullable=True)
    probe_id = Column(Integer,nullable=True)
    maintenance_mode = Column(Enum(Maintenance), default=Maintenance.n)
    status = Column(Enum(Status),default=Status.y)
    date_modified = Column(DateTime(timezone=True),server_default=func.now(),onupdate = func.now())
    date = Column(DateTime(timezone=True), server_default=func.now())

class monitoring(Base):
    __tablename__ = 'monitoring'
    interval_id = Column(BigInteger,primary_key=True, autoincrement=True)
    monitor_interval = Column(Integer,nullable=True)
    initial_alert_time = Column(Integer,nullable=True)
    repeated_alert_time = Column(Integer,nullable=True)
    collector_next_check_time =  Column(DateTime(timezone = True))
    reader_next_check_time = Column(DateTime(timezone = True))
    monitor_type_id = Column(BigInteger, nullable=True)
    app_host_id = Column(Integer, ForeignKey('app_host.app_host_id'))
    date_modified = Column(DateTime(timezone = True), onupdate = func.now(), server_default=func.now())
    date = Column(DateTime(timezone = True), server_default=func.now())









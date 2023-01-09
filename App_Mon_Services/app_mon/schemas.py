from pydantic import BaseModel,Field
from datetime import datetime
import enum
from typing import Union

class Status(str,enum.Enum):
    y = 'y'
    n = 'n'

class app_mon(BaseModel):
    app_name: str = Field(..., regex="^[a-zA-Z][a-zA-Z0-9- _]*$", max_length=255)
    app_key: str = Field(..., regex='^[A-Z0-9]+(?:_[A-Z0-9]+)*$', max_length=255)
    status:str = "y"
    monitor_interval : int
    initial_alert_time : int 
    repeated_alert_time : int 
    class Config():
        orm_mode =True
        schema_extra ={
            "example":{
                "app_name" : "",
                "app_key" : "",
                "monitor_interval" : "",
                "initial_alert_time" : "",
                "repeated_alert_time" : ""
            }
        }

class ShowApp(BaseModel):
    app_name: str
    app_key: str
    status:enum.Enum   
    date_modified:datetime
    date:datetime
    monitor_interval:int
    initial_alert_time:int
    repeated_alert_time: int
    class Config():
        orm_mode =True

class monitor(BaseModel):
    monitor_interval : int
    initial_alert_time : int
    repeated_alert_time : int
    # collector_next_check_time : int
    # reader_next_check_time : int
    monitor_type_id :int
    app_host_id : int
    class Config():
        orm_mode =True
        schema_extra ={
            "example":{
                "monitor_interval" : "",
                "initial_alert_time" : "",
                "repeated_alert_time" : "",
                "monitor_type_id" : "",
                "app_host_id" : ""
            }
        }

class ShowMon(BaseModel):
    monitor_interval : int
    initial_alert_time : int
    repeated_alert_time : int
    monitor_type_id :int
    app_host_id : int
    date_modified :datetime
    date : datetime
    class Config():
        orm_mode =True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str  
    class Config():
        orm_mode =True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

class App_host(BaseModel):
    app_id : int
    app_host_name : str = Field(..., max_length=255,regex="^[a-zA-Z][a-zA-Z0-9- _]*$") 
    project_id : str = Field(...,max_length=255,regex='^[A-Z0-9]+(?:_[A-Z0-9]+)*$')
    ip : str = Field(...)
    port : int = Field(...)
    cred_req : str = "y"
    user_name : str
    password : str
    app_req_url : str =Field(regex="((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
    app_instance : str
    service_status : str = "y"
    service_status_details : str
    monitor_method : str
    probe_id : int
    maintenance_mode : str = "n"
    status : str = "y"  
    class Config():
        orm_mode=True  
        schema_extra = {
            "example": {
                    "app_id" : "",
                    "app_host_name" : "",
                    "project_id" : "",
                    "ip" : "",
                    "port" : "",
                    "user_name" : "",
                    "password" : "",
                    "app_req_url" : "",
                    "app_instance" : "",
                    "service_status_details" : "",
                    "monitor_method" : "",
                    "probe_id" : "",
                        
                    }
                }

class Showapphost(BaseModel):
    app_host_id : int
    app_id = int
    app_host_name : str 
    project_id : str
    ip : str
    port : int
    cred_req : enum.Enum
    user_name : str
    #password : str
    app_req_url : str
    app_instance : str
    service_status : enum.Enum
    service_status_details : str
    monitor_method : str
    probe_id : int
    maintenance_mode : enum.Enum
    status : enum.Enum
    date_modified : datetime
    date : datetime

    class Config():
        orm_mode=True

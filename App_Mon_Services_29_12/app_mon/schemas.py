from pydantic import BaseModel,Field
from datetime import datetime
import enum


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
    # collector_next_check_time : datetime
    # reader_next_check_time : datetime
    monitor_type_id :int
    app_host_id : int
    date_modified :datetime
    date : datetime
    class Config():
        orm_mode =True
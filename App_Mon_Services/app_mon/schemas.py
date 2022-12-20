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
    class Config():
        orm_mode =True
        schema_extra ={
            "example":{
                "app_name" : "",
                "app_key" : "",
            }
        }


class ShowApp(BaseModel):
    app_name: str
    app_key: str
    status:enum.Enum   
    date_modified:datetime
    date:datetime
    class Config():
        orm_mode =True


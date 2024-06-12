from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra ={
            "example":{
                "email":"sample@email.com",
                "password":"pw12345"
            }
        }
        
class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra ={
            "example":{
                "email":"sample@email.com",
                "password":"pw12345"
            }
        }
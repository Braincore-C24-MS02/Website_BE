from pydantic import BaseModel


class SignUpSchema(BaseModel):
    name: str  # Menambahkan bidang name
    email: str
    password: str
    
    class Config:
        json_schema_extra ={
            "example":{
                "name": "John Doe",  # Contoh data untuk bidang name
                "email": "sample@email.com",
                "password": "pw12345"
            }
        }
        
class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra ={
            "example":{
                "email": "sample@email.com",
                "password": "pw12345"
            }
        }

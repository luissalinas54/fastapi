from fastapi import FastAPI
from pydantic import BaseModel          #DEFINIMOS LA ENTDIDAD 



app = FastAPI()

#INICIAR EL SERVER: uvicorn users:app --reload

#DEFINIMOS LA ENTIDAD/OBJETO USER

class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int

#DEFINIMOS LISTA CON DISTINTOS USUARIOS
users_list = [User(name="Luis" , surname="Salinas", url="http://google.com", age=26),
                User(name="Sebastian" , surname="Salinas", url="http://youtube.com", age=24),
                User(name="Emilio" , surname="Salinas", url="http://facebook.com", age=20)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Luis", "surname" : "Salinas", "url" : "http://googele.com", "age" : 26 },
           {"name": "Sebastian", "surname" : "Salinas", "url" : "http://youtube.com", "age" : 24 },
           {"name": "Emilio", "surname" : "Salinas", "url" : "http://facebook.com" , "age" : 20} ]

@app.get("/users")
async def users():
    return users_list
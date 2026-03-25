from fastapi import FastAPI
from pydantic import BaseModel          #DEFINIMOS LA ENTDIDAD 



app = FastAPI()

#INICIAR EL SERVER: uvicorn users:app --reload

#DEFINIMOS LA ENTIDAD/OBJETO USER

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

#DEFINIMOS LISTA CON DISTINTOS USUARIOS
users_list = [User(id = 1, name="Luis" , surname="Salinas", url="http://google.com", age=26),
                User(id = 2, name="Sebastian" , surname="Salinas", url="http://youtube.com", age=24),
                User(id = 3, name="Emilio" , surname="Salinas", url="http://facebook.com", age=20)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Luis", "surname" : "Salinas", "url" : "http://googele.com", "age" : 26 },
           {"name": "Sebastian", "surname" : "Salinas", "url" : "http://youtube.com", "age" : 24 },
           {"name": "Emilio", "surname" : "Salinas", "url" : "http://facebook.com" , "age" : 20} ]

@app.get("/users")
async def users():
    return users_list

#----------------------------------------------------------------------------
#FILTRAMOS LOS USURIOS DESDE EL PROPIO PATH DE AL URL 
#los {} SIGNIFICA QUE SON LOS PARAMETROS A CAPTURAR DE USERS
#http://127.0.0.1:8000/user/1

@app.get("/user/{id}")
async def user(id: int):
   return search_users(id)

#USAMOS LA QUERY (IGUALAR CLAVE A UN VALOR DE LA URL)
#http://127.0.0.1:8000/useruserquery/?id=1

@app.get("/userquery/")
async def user(id: int):
    return search_users(id)
    

#DEFINIMOS LA FUNCION PARA VER SI EXISTE EL USUARIO
def search_users(id:int):
    users  = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error" : "No se ha encontrado al usuario"}
    
#USAMOS EL PATH PARA VALORES QUE SON INDISPENSABLES Y QUERY PARA VALORES DINAMICOS
#EN UNA BASE DE DATOS LA PAGINACION (CARGAR ELEMENTOS/ USUARIOS DEL 1 AL 10) SE UTILIZA LA QUERY
#EN UNA BASE DE DATOS EL NOMBRE (ID) DE UNA BASE ES FIJA Y TIENE QUE SER POR EL PATH

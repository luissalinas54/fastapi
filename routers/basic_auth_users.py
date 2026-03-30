from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# uvicorn basic_auth_users:app --reload
#Url local : http://127.0.0.1:8000
app = FastAPI()

#isntancia de la clase OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool 

class UserDB(User):
    password: str

# USUARIO EN UNA BASE DE DATOS
users_db = {
    "luis" : {
        "username": "luis",
        "full_name": "Luis Salinas",
        "email": "luchoaldo555a@gmail.com",
        "disabled": False,
        "password": "12345"
    },

    "sebas" : {
        "username": "sebas",
        "full_name": "Sebastián Salinas",
        "email": "sebas.salinas@gmail.com",
        "disabled": True,
        "password": "54231"
    }

}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

#CREAMOS EL CRITERIO DE DEPENDENCIA PARA VER SI EL USUARIO ESTA AUTENTICADO O NO
async def current_user(token : str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autentificacion invalidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")

    return user


#HACEMOS LA AUTENTICACION DE USUARIOS
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    #BUSCAMOS EL USUARIO EN LA BASE DE DATOS
    user_db = users_db.get(form.username)

    #COMPROBAMOS SI EL USUARIO EXISTE EN LA BASE DE DATOS
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    #AQUI DEVOLVEMOS EL USUARIO SI EXISTE 
    user = search_user_db(form.username)

    #VERIFICAMOS SI LA CONTRASEÑA ES CORRECTA
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    #SI ES CORRECTO DEVOLVEMOS EL TOKEN
    return {"access_token": user.username, "token_type": "bearer"}

#OPERACION PARA DEVOLVER LOS DATOS DE USUARIO AUTENTICADO
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    
    return user
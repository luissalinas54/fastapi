import token

from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#IMPORTACIONES PARA EL JWT
from jose import jwt 
from jose.exceptions import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

#ALGORITMO PARA ENCRIPTAR EL TOKEN
ALGORITHM = "HS256"
#DURACION DEL ACCESS TOKEN (1 minuto)
ACCESS_TOKEN_DURATION = 1

#CREAMOS UNA CLAVE SECRETA PARA ENCRIPTAR EL TOKEN
#openssl rand -hex 32
SECRET= "75a03166acff4e79adeac521dab6ce05111002f012d946ee2db7ffc2989537d6"

#cd routers
# uvicorn jwt_auth_users:app --reload
#Url local : http://127.0.0.1:8000


router = APIRouter()

#isntancia de la clase OAuth2PasswordBearer para usuario y contraseña
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#CONTEXTO DE INCRIPTACION PARA EL TOKEN
crypt = CryptContext(schemes=["bcrypt"])

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
        #"password": "12345"
        "password": "$2a$12$zRPprG7F91v9cfXRq5LbvebM8JjOOv5T9PFCWcnRxv2L98KA8Ddsi"
    },

    "sebas" : {
        "username": "sebas",
        "full_name": "Sebastián Salinas",
        "email": "sebas.salinas@gmail.com",
        "disabled": True,
        #"password": "54231"
        "password": "$2a$12$.upq8/mDw4HRqWLhyJaG9.8u0/XJ3CpDCR9rzTJ/DlRUihn3UrSD6"
    }
}


#BUSCAMOS USUARIO CON CONTRASEÑA
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
#BUSCAMOS USUARIO SIN CONTRASEÑA    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

#DEFINIMOS UN CRITERIO DE BUSQUEDA PARA EL USUARIO EN LA BASE DE DATOS
async def auth_user(token : str = Depends(oauth2)):

#CREAMOS UNA VARIABLE PARA LA EXCEPCION DE AUTENTICACION INVALIDA
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autentificacion invalidas",
        headers={"WWW-Authenticate": "Bearer"})

#AQUI DECODIFICAMOS EL TOKEN PARA OBTENER EL USUARIO Y VER SI EL TOKEN ES VALIDO O NO
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        #EN CASO DE QUE EL NOMBRE DE USUARIO ESTE VACIO O NO EXISTA EN LA BASE DE DATOS DEVOLVEMOS UN ERROR DE AUTENTICACION
        if username is None:
            raise exception
        
    except JWTError:
        raise exception

    return search_user(username)


#CREAMOS EL CRITERIO DE DEPENDENCIA PARA VER SI EL USUARIO ESTA AUTENTICADO O NO
async def current_user(user : User = Depends(auth_user)):
     
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")

    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    #BUSCAMOS EL USUARIO EN LA BASE DE DATOS
    user_db = users_db.get(form.username)

    #COMPROBAMOS SI EL USUARIO EXISTE EN LA BASE DE DATOS
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    #AQUI DEVOLVEMOS EL USUARIO SI EXISTE 
    user = search_user_db(form.username)

    #VERIFICAMOS SI LA CONTRASEÑA ES CORRECTA UTILIZANDO EL CONTEXTO DE ENCRIPTACION

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    

    #CALCULAMOS EL TIEMPO DE DURACION DEL TOKEN
    #datetime.utcnow es la fecha y hora actual en formato UTC del sistema

    expired = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    #CREASMOS EL OBJECTO DEL TOKEN CON LOS PARAMETROS NECESARIOS PARA LA CREACION DEL TOKEN (NOMBRE, CONTRAEAÑA Y TIEMPO DE DURACION)

    access_token = {
        "sub": user.username,
        "exp": expired
    }

    #SI ES CORRECTO DEVOLVEMOS EL TOKEN
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    
    return user
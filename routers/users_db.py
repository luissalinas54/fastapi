from fastapi import APIRouter, status, HTTPException
from db.models.users import User
#IMPORTAMOS EL CLIENTE DB
from db.client import db_Client
from schemas.user import user_schem, users_schema
from bson import ObjectId

#UTILIZAMOS EL TAG PARA AGRUPAR CADA METODO CON LA ROUTE A LA QUE CORRESPINDE EN LA DOCIMENTACION
router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses= {status.HTTP_404_NOT_FOUND : {"message" : "no encontrado"}})


#METODOS GET PARA OBTENER LOS USUARIOS DE LA BASE DE DATOS
@router.get("/", response_model= list[User])
async def users():
    return users_schema(db_Client.users.find())

@router.get("/{id}")
async def user(id: str):
   return search_user("_id", ObjectId(id))

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# METODO POST   http://127.0.0.1:8000/user

@router.post("/", response_model= User,status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user("email", user.email))== User:
        raise HTTPException(
            status.HTTP_201_CREATED,
            detail="El usuario ya existe")

    #TRNSFORMAMOS LA ENTIDIAD USER EN UN DICCIONARIO (ESTO ES UN JSON) PARA PODER GUARDARLO EN LA BASE DE DATOS
    user_dict = dict(user)
    #ELIMINAMOS EL CAMPO ID DEL DICCIONARIO (ESTO ES UN JSON) PARA PODER GUARDARLO EN LA BASE DE DATOS
    #EL ID LO AUTOGESTIONA MONGODB
    del user_dict["id"]

    #INSERTAMOS EL USUARIO EN LA BASE DE DATOS (USAMOS EL CLIENTE DB)
    id = db_Client.users.insert_one(user_dict).inserted_id

    #ACCEDEMOS A LA BASE DE DATOS PARA VER SI SE HA GUARDADO EL USUARIO Y LE ASIGNAMOS EL ID QUE NOS HA DADO LA BASE DE DATOS
    #fin one ENCUENTRA UN JSON POR LO QUE NECESITAMOS TRANSFORMARLO EN UN OBJETO DE LA CLASE USER PARA PODER DEVOLVERLO EN LA RESPUESTA

    new_user = user_schem(db_Client.users.find_one({"_id": id}))

    #RETORNAMOS UN NUEVO USUARIO OASANDOLE TODAS LAS CLAVES DEL DICCIONARIO 
    return User(**new_user)


# METODO PUT http://127.0.0.1:8000/user

@router.put("/", response_model= User)
async def user(user:User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_Client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error" : "No se ha actualizado al usuario"}

    return search_user("_id", ObjectId(user.id))          
    

#DELETE http://127.0.0.1:8000/users/4
#AQUI USAMOS EL PTH PORQUE EL ID ES OBLIGATORIO
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_Client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error" : "No se ha eliminado al usuario"}
    else:
        return user 


#DEFINIMOS LA FUNCION PARA VER SI EXISTE EL USUARIO
#LE PONEMOS EL FIELD Y KEY PARA HACERLO GENERICO, NOSOTROS PASAMOS LOS CAMPOS QUE QUEREMOS USAR
def search_user(field: str, key):
    
    try:
        user = db_Client.users.find_one({field: key})
        return User(**user_schem(user))
    except:
        return {"error" : "No se ha encontrado al usuario"}
    
#USAMOS EL PATH PARA VALORES QUE SON INDISPENSABLES Y QUERY PARA VALORES DINAMICOS
#EN UNA BASE DE DATOS LA PAGINACION (CARGAR ELEMENTOS/ USUARIOS DEL 1 AL 10) SE UTILIZA LA QUERY
#EN UNA BASE DE DATOS EL NOMBRE (ID) DE UNA BASE ES FIJA Y TIENE QUE SER POR EL PATH

def search_users(id: int):
    return ""
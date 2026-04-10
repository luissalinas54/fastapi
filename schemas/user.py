#CREAMOS LA FUNCION PARA QUE NOS DEVUELVA UN USUARIO POR SU ID
#el campo id es un objeto de tipo ObjectId, por lo que lo convertimos a string para que sea mas facil de manejar
def user_schem(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
        }

#CREAMOS LA FUNCION PARA QUE NOS DEVUELVA UNA LISTA DE USUARIOS

def users_schema(users) -> list:
    return [user_schem(user) for user in users]


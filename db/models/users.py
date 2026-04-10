from pydantic import BaseModel

class User(BaseModel):
    #CON none DECIMOS QUE EL ID NO ES OBLIGATORIO,
    #YA QUE CUANDO CREAMOS UN USUARIO NUEVO NO VAMOS A SABER SU ID (SE LO ASIGNA LA BASE DE DATOS)
    id: str | None = None
    username: str
    email: str
 
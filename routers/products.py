from fastapi import APIRouter
from pydantic import BaseModel   

#UTILIZAMOS EL TAG PARA AGRUPAR CADA METODO CON LA ROUTE A LA QUE CORRESPINDE EN LA DOCIMENTACION
router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses= {404 : {"message" : "no encontrado"}})

# uvicorn products:app --reload


class Product(BaseModel):
    id: int
    name: str
  


products_list = [
    {"id": 1, "name": "Producto 1"},
    {"id": 2, "name": "Producto 2"},
    {"id": 3, "name": "Producto 3"},
    {"id": 4, "name": "Producto 4"}
]

@router.get("/")
async def products():
    return products_list

from fastapi import HTTPException

@router.get("/{id}", response_model=Product, status_code=200)
async def get_product(id: int):
    product = search_product(id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return product



#DEFINIMOS LA FUNCION PARA VER SI EXISTE EL PRODUCTO
def search_product(id:int):
    return next((p for p in products_list if p["id"] == id), None)
    
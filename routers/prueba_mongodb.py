from pymongo import MongoClient

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://luis:luis171299@cluster0.1qmcpmo.mongodb.net/")

# Base de datos
db = client["mi_app"]

# Colección
collection = db["users"]

# Insertar un documento
collection.insert_one({
    "nombre": "Luis",
    "edad": 25
})

print("Dato insertado correctamente")

# Mostrar bases de datos
print(client.list_database_names())

# Mostrar documentos de la colección
for doc in collection.find():
    print(doc)
from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests

		
def getProductos():
    api_url = 'https://fakestoreapi.com/products'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanzar una excepción si la solicitud no es exitosa

        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []

# Conexión con la BD				
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
				
data = getProductos()
    
if data:
    productos_collection.insert_many(data) 	

# Consulta 1: Electrónica entre 100 y 200€, ordenados por precio
electronicos_entre_100_y_200 = productos_collection.find({
    'category': 'electronics',
    'price': {'$gte': 100, '$lte': 200}
}).sort('price')

print("---------Productos de Electrónica entre 100 y 200€ ordenados por precio:--------------")
for producto in electronicos_entre_100_y_200:
    print(producto.get('title'), '| Categoría:', producto.get('category'), '| Precio:', producto.get('price'))

# Consulta 2: Productos que contengan la palabra 'pocket' en la descripción
productos_con_pocket = productos_collection.find({
    'description': {'$regex': 'pocket', '$options': 'i'}
})

print("\n----------Productos con la palabra 'pocket' en la descripción:------------------")
for producto in productos_con_pocket:
    print(producto.get('title'), '| Description:', producto.get('description'))
     
# Consulta 3: Productos con puntuación mayor de 4
productos_con_puntuacion_mayor_4 = productos_collection.find({
    'rating.rate': {'$gt': 4}
}).sort('rating.rate', 1)

print("\n-----------------------Productos con puntuación mayor de 4:------------------")
for producto in productos_con_puntuacion_mayor_4:
    print(producto.get('title'), '| Puntuación:', producto["rating"]["rate"])

# Consulta 4: Ropa de hombre, ordenada por puntuación
ropa_hombre_ordenada_por_puntuacion = productos_collection.find({
    "category":"men's clothing"
}).sort('rating.rate', -1)

print("\n------------------------Ropa de hombre ordenada por puntuación:------------------")
for producto in ropa_hombre_ordenada_por_puntuacion:
    print(producto.get('title'), '| Categoría:', producto.get('category'), '| Puntuación:', producto["rating"]["rate"])


# Consulta 5: Facturación total
fact_total = [
    {
        '$group': {
            '_id': None,
            'totalRevenue': {'$sum': '$price'}
        }
    }
]

fact_total = productos_collection.aggregate(fact_total)

for result in fact_total:
    f_total = result['totalRevenue']

print(f"---------------Facturación total: {f_total} €---------------")


# Consulta 6: Facturación por categoría de producto
fact_categ = [
    {
        '$group': {
            '_id': '$category',
            'totalRevenue': {'$sum': '$price'}
        }
    }
]

fact_categ = productos_collection.aggregate(fact_categ)

print("---------------------Facturación por categoría:--------------------")
for result in fact_categ:
    category = result['_id']
    f_category = result['totalRevenue']
    if category != None:
        print(f"{category}: {f_category} €")

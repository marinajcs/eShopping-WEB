from pydantic import BaseModel, FilePath, Field, EmailStr, ValidationError
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
from django.db import models

		
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
def electronicos_entre_100_y_200():
    electronicos_entre_100_y_200 = productos_collection.find({
        'category': 'electronics',
        'price': {'$gte': 100, '$lte': 200}
    }).sort('price')

    output = "<h3>Productos de Electrónica entre 100 y 200€ ordenados por precio</h3>"
    for producto in electronicos_entre_100_y_200:
        output += f"{producto.get('title')} | Categoría: {producto.get('category')} | Precio: {producto.get('price')} <br>"

    return output

# Consulta 2: Productos que contengan la palabra 'pocket' en la descripción
def productos_pocket():
    productos_con_pocket = productos_collection.find({
        'description': {'$regex': 'pocket', '$options': 'i'}
    })

    output = ("<h3>Productos con la palabra 'pocket' en la descripción:</h3>")
    for producto in productos_con_pocket:
        output += f"{producto.get('title')} | Description: {producto.get('description')} <br>"
       
    return output
 
# Consulta 3: Productos con puntuación mayor de 4
def puntuacion_mayor_4():
    productos_con_puntuacion_mayor_4 = productos_collection.find({
        'rating.rate': {'$gt': 4}
    }).sort('rating.rate', 1)

    output = ("<h3>Productos con puntuación mayor de 4:</h3>")
    for producto in productos_con_puntuacion_mayor_4:
        output += f"{producto.get('title')} | Puntuación: {producto['rating']['rate']}) <br> <br>"

    return output

# Consulta 4: Ropa de hombre, ordenada por puntuación
def ropa_hombre_puntuacion():
    ropa_hombre_ordenada_por_puntuacion = productos_collection.find({
        "category":"men's clothing"
    }).sort('rating.rate', -1)

    output = ("<h3>Ropa de hombre ordenada por puntuación</h3>")
    for producto in ropa_hombre_ordenada_por_puntuacion:
        output += f"{producto.get('title')} | Categoría: {producto.get('category')} | Puntuación: {producto['rating']['rate']} <br>"

    return output

# Consulta 5: Facturación total
def facturacion_total():
    fact_total = [
        {
            '$group': {
                '_id': None,
                'totalRevenue': {'$sum': '$price'}
            }
        }
    ]

    fact_total = productos_collection.aggregate(fact_total)
    output = ""
    for result in fact_total:
        output += f"<h3>Facturación total: {result['totalRevenue']} €</h3>"

    return output


# Consulta 6: Facturación por categoría de producto
def facturacion_categoria():
    fact_categ = [
        {
            '$group': {
                '_id': '$category',
                'totalRevenue': {'$sum': '$price'}
            }
        }
    ]

    fact_categ = productos_collection.aggregate(fact_categ)

    output = "<h3>Facturación por categoría</h3>"
    for result in fact_categ:
        category = result['_id']
        f_category = result['totalRevenue']
        if category != None:
            output += f"{category}: {f_category} € <br>"
    
    return output

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


def productos_con_palabra_clave(palabra_clave):
    productos_con_clave = productos_collection.find({
        '$or': [
            {'description': {'$regex': palabra_clave, '$options': 'i'}},
            {'title': {'$regex': palabra_clave, '$options': 'i'}}
        ]
    })

    return productos_con_clave

 
def productos_por_categoria(categoria):
    prod_por_categ = productos_collection.find({
        "category":categoria
    })

    return prod_por_categ

from pymongo import MongoClient
import requests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def save_uploaded_image(uploaded_image):
    # Guarda el archivo en la carpeta de media con un nombre único
    file_name = default_storage.save(os.path.join('images', uploaded_image.name), ContentFile(uploaded_image.read()))
    return file_name

def get_image_url(file_name):
    # Construye la URL de la imagen basada en MEDIA_URL y el nombre del archivo
    media_url = settings.MEDIA_URL
    if not media_url.endswith('/'):
        media_url += '/'
    return f"{media_url}{file_name}"
		
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
				
productos_collection.delete_many({})

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
    logger.info(f"Búsqueda por palabra clave '{palabra_clave}' realizada.")

    return productos_con_clave

 
def productos_por_categoria(categoria):
    prod_por_categ = productos_collection.find({
        "category":categoria
    })
    logger.info(f"Listado por categoría '{categoria}' realizado.")
    
    return prod_por_categ

def insertar_producto(titulo, descripcion, precio, categoria, imagen):
    img_path = save_uploaded_image(imagen)
    img_url = get_image_url(img_path)

    # Crea un documento JSON con los datos del producto
    producto_data = {
        "title": titulo,
        "description": descripcion,
        "price": float(precio),  # Convierte DecimalField a float
        "category": categoria,
        "image": img_url,
    }
    logger.info(f"Nuevo producto '{titulo}' insertado en la base de datos.")

    # Inserta el documento en la colección de MongoDB
    productos_collection.insert_one(producto_data)
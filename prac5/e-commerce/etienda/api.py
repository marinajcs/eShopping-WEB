from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from ninja.security import HttpBasicAuth
from etienda.models import productos_collection
from bson import ObjectId
import logging
from pymongo import ASCENDING
from typing import List
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Logger
logger = logging.getLogger(__name__)

# API
api = NinjaExtraAPI(csrf=True)

# Autenticación
class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == "marina" and password == "password0":
            return username


# - - - - - - - - - - - - - - - - MATES - - - - - - - - - - - - - - - -
# function based definition
"""@api.get("/add", tags=["Aritmética"])
def add(request, a: int, b: int):
    return {"ok": "yes", "data": {"suma": a + b, "resta": a - b}}
"""


# class based definition
@api_controller("/math", tags=["Aritmética"], auth=BasicAuth())
class math:
    # Suma
    @http_get("/add")
    def add(self, request, a: int, b: int):
        return {"ok": "yes", "data": a + b}

    # Resta
    @http_get("/subtract")
    def subtract(self, request, a: int, b: int):
        return {"ok": "yes", "data": a - b}

    # Multiplicación
    @http_get("/multiply")
    def multiply(self, request, a: int, b: int):
        return {"ok": "yes", "data": a * b}

    # División
    @http_get("/divide")
    def divide(self, request, a: int, b: int):
        return {"ok": "yes", "data": a / b}

    # Potencia
    @http_get("/power")
    def power(self, request, a: int, b: int):
        return {"ok": "yes", "data": a**b}

    # Raíz cuadrada
    @http_get("/sqrt")
    def sqrt(self, request, a: int):
        return {"ok": "yes", "data": a**0.5}


# Registrar el controlador
api.register_controllers(math)

# - - - - - - - - - - - - - - - - TIENDA DAI - - - - - - - - - - - - - - - -


class Rate(Schema):
    rate: float
    count: int


class ProductSchema(Schema):  # sirve para validar y para documentación
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate


class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate


class ErrorSchema(Schema):
    message: str


# Prueba de conexión a la base de datos
@api.get("/ping", tags=["TIENDA DAI"], auth=BasicAuth())
def ping(request):
    try:
        # Contar los documentos de la colección de productos
        productos_collection.estimated_document_count()
        logger.info("Conexión a la base de datos exitosa")

        return 200, {"message": "pong"}
    except Exception as e:
        logger.info("Error al conectar a la base de datos: {e}")
        return 500, {"message": "error al conectar a la base de datos"}


# - - - - - - - - - - - - - - - - CRUD - - - - - - - - - - - - - - - -


# Crear producto (C)
@api.post(
    "/productos",
    tags=["TIENDA DAI"],
    response={201: ProductSchema, 400: ErrorSchema},
    auth=BasicAuth(),
)
def Crea_producto(request, payload: ProductSchemaIn):
    try:
        # Crear un nuevo producto con los datos de payload
        resu = productos_collection.insert_one(payload.dict())

        # Convertir a diccionario y realizar modificaciones
        payload_dict = payload.dict()

        # Verificar si '_id' está presente antes de intentar eliminarlo
        if "_id" in payload_dict:
            del payload_dict["_id"]

        # Agregar el nuevo 'id' al diccionario
        payload_dict["id"] = str(resu.inserted_id)

        datos_producto = ProductSchema(**payload_dict)

        logger.info(f"Producto creado: {payload_dict['id']}")
        return 201, datos_producto
    except Exception as e:
        logger.info(f"Error al crear producto: {e}")
        return 400, {"message": "error al crear producto"}


# Leer producto (R)
@api.get(
    "/productos/{id}",
    tags=["TIENDA DAI"],
    response={200: ProductSchema, 404: ErrorSchema},
    auth=BasicAuth(),
)
def Lee_producto(request, id: str):
    try:
        # Buscar desde el string id
        resu = productos_collection.find_one({"_id": ObjectId(id)})

        if resu:
            # Añadir "id" desde "_id"
            resu["id"] = str(resu.get("_id"))
            del resu["_id"]

            logger.info(f"Producto leído: {resu['id']}")
            return 200, resu
        else:
            return 404, {"message": "producto no encontrado"}
    except Exception as e:
        logger.info(f"Error al leer producto: {e}")
        return 404, {"message": "error al leer producto"}


# Actualizar producto (U)
@api.put(
    "/productos/{id}",
    tags=["TIENDA DAI"],
    response={202: ProductSchema, 404: ErrorSchema},
    auth=BasicAuth(),
)
def Modifica_producto(request, id: str, payload: ProductSchemaIn):
    try:
        # Buscar desde el string id
        resu = productos_collection.find_one({"_id": ObjectId(id)})

        if resu:
            # Actualizar los campos según payload
            for attr, value in payload.dict().items():
                logger.debug(f"{attr} -> {value}")
                # modificar DB
                resu[attr] = value

            # Guardar los cambios en la base de datos
            productos_collection.replace_one({"_id": ObjectId(id)}, resu)

            # Añadir "id" desde "_id"
            resu["id"] = str(resu.get("_id"))
            del resu["_id"]

            logger.info(f"Producto modificado: {resu['id']}")
            return 202, resu
        else:
            return 404, {"message": "no encontrado"}
    except Exception as e:
        logger.info(f"Error al modificar producto: {e}")
        return 404, {"message": "error al modificar"}


# Eliminar producto (D)
@api.delete(
    "/productos/{id}",
    tags=["TIENDA DAI"],
    response={204: None, 404: ErrorSchema},
    auth=BasicAuth(),
)
def Elimina_producto(request, id: str):
    try:
        # Eliminar desde el string id y obtener el resultado
        resu = productos_collection.delete_one({"_id": ObjectId(id)})

        if resu.deleted_count > 0:
            logger.info(f"Producto eliminado: {id}")
            return 204, None
        else:
            return 404, {"message": "Producto no encontrado"}
    except Exception as e:
        logger.info(f"Error al eliminar producto: {e}")
        return 404, {"message": "Error al eliminar producto"}


# Lista productos con paginador
@api.get(
    "/productos",
    tags=["TIENDA DAI"],
    response={200: List[ProductSchema], 404: ErrorSchema},
    auth=BasicAuth(),
)
def Lista_productos(request, desde: int, hasta: int):
    try:
        # Obtener los productos desde la base de datos
        resu = productos_collection.find().skip(desde * hasta).limit(hasta)

        # Convertir a lista
        resu = list(resu)

        # Añadir "id" desde "_id"
        for prod in resu:
            prod["id"] = str(prod.get("_id"))
            del prod["_id"]

        logger.info(f"Productos listados")
        return 200, resu
    except Exception as e:
        logger.info(f"Error al listar productos: {e}")
        return 404, {"message": "Error al listar productos"}

# Actualizar rating
@api.put(
    "/productos/{id}/rating/{newRating}",
    tags=["TIENDA DAI"],
    response={202: ProductSchema, 404: ErrorSchema},
)
def Actualiza_rating(request, id: str, newRating: int):
    try:
        # Buscar desde el string id
        resu = productos_collection.find_one({"_id": ObjectId(id)})

        if resu:
            # Actualizar la calificación y el recuento de votos
            nuevaPuntuacionMedia = (resu["rating"]["rate"] * resu["rating"]["count"] + newRating) / (resu["rating"]["count"] + 1)
            resu["rating"]["rate"] = round(nuevaPuntuacionMedia, 2)
            resu["rating"]["count"] += 1

            # Guardar los cambios en la base de datos
            productos_collection.replace_one({"_id": ObjectId(id)}, resu)

            # Añadir "id" desde "_id"
            resu["id"] = str(resu.get("_id"))
            del resu["_id"]

            logger.info(f"Rating modificado: {resu['id']}")
            return 202, resu
        else:
            return 404, {"message": "no encontrado"}
    except Exception as e:
        logger.info(f"Error al actualizar rating: {e}")
        return 404, {"message": "error al actualizar rating"}

# Ruta para obtener productos que contienen la palabra de búsqueda en el título o descripción
@csrf_exempt
@api.get("/productos/buscar/", tags=["TIENDA DAI"], response=List[ProductSchema])
def buscar_productos(request, palabraClave: str):
    try:
        # Buscar productos que contienen la palabra de búsqueda en el título o descripción
        resultados = productos_collection.find({
            "$or": [
                {"titulo": {"$regex": palabraClave, "$options": "i"}},
                {"descripcion": {"$regex": palabraClave, "$options": "i"}},
            ]
        })

        # Procesar resultados y convertir a lista de ProductSchema
        productos = []
        for producto in resultados:
            producto["id"] = str(producto["_id"])
            del producto["_id"]
            productos.append(ProductSchema(**producto))

        logger.info(f"Productos encontrados para la búsqueda: {palabraClave}")
        return productos

    except Exception as e:
        logger.error(f"Error al buscar productos: {e}")
        return 404, {"message": "error al buscar productos"}
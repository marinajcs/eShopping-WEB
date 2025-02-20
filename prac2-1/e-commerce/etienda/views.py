from django.shortcuts import render
from django.http import HttpResponse
#from app.models import #nombre de funcion de consulta
from etienda.models import *

# Create your views here.
def index(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Índice de consultas</title>
    </head>
    <body>
    <h1>Índice de consultas</h1>
        <ul>
            <li><a href="/etienda/consulta1">Consulta electrónica</a></li>
            <li><a href="/etienda/consulta2">Consulta pocket</a></li>
            <li><a href="/etienda/consulta3">Consulta puntuación mayor a 4</a></li>
            <li><a href="/etienda/consulta4">Consulta ropa hombre puntuación</a></li>
            <li><a href="/etienda/consulta5">Facturación total</a></li>
            <li><a href="/etienda/consulta6">Facturación por categoría</a></li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html_content)


def consulta_electronica(request):
    res = electronicos_entre_100_y_200()
    return HttpResponse(res)

def consulta_pocket(request):
    res = productos_pocket()
    return HttpResponse(res)

def consulta_puntuacion_mayor_4(request):
    res = puntuacion_mayor_4()
    return HttpResponse(res)

def consulta_ropa_hombre_puntuacion(request):
    res = ropa_hombre_puntuacion()
    return HttpResponse(res)

def consulta_facturacion_total(request):
    res = facturacion_total()
    return HttpResponse(res)

def consulta_facturacion_categoria(request):
    res = facturacion_categoria()
    return HttpResponse(res)
from django.shortcuts import render
from django.http import HttpResponse
from etienda.models import *

# Create your views here.


def index(request):
    contexto = {'variable': 'Valor de ejemplo'}
    
    return render(request, './ofertas.html')

def search_results(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Obtén el término de búsqueda de la URL
        # Realiza la búsqueda en tus datos y obtén los resultados
        resultados = productos_con_palabra_clave(query)
        return render(request, './busqueda.html', {'resultados': resultados, 'query': query})
    
def categories_results(request, category_name):
    resultados = productos_por_categoria(category_name)
    
    return render(request, './categoria.html', {'resultados': resultados, 'category_name': category_name})
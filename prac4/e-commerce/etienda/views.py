from django.shortcuts import render
from django.http import HttpResponse
from etienda.models import *
from etienda.forms import ProductForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    
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

@login_required(login_url='/etienda/login')
def new_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Aquí puedes acceder a los datos del formulario y procesarlos como desees
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            
            insertar_producto(title, description, price, category, image)
    
    return render(request, './nuevo-producto.html', {'form': form})

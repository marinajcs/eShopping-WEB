from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search_results, name='search_results'),
    path('category/<str:category_name>/', views.categories_results, name='category_results'),
]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .api import api

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.search_results, name='search_results'),
    path('category/<str:category_name>/', views.categories_results, name='category_results'),
    path('add-product/', views.new_product , name='show_form'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/", api.urls),

]
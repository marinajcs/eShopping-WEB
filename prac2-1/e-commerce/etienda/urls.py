from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("consulta1", views.consulta_electronica, name="consulta1"),
    path("consulta2", views.consulta_pocket, name="consulta2"),
    path("consulta3", views.consulta_puntuacion_mayor_4, name="consulta3"),
    path("consulta4", views.consulta_ropa_hombre_puntuacion, name="consulta4"),
    path("consulta5", views.consulta_facturacion_total, name="consulta5"),
    path("consulta6", views.consulta_facturacion_categoria, name="consulta6"),
]
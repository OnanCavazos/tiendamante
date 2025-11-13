# Principal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ruta del catálogo general de la app (http://.../catalogo/)
    path("catalogo/", views.catalogo, name="catalogo"),

    # contacto y guardado de contacto (form)
    path("contacto/", views.contacto, name="contacto"),
    path("contacto/guardar/", views.guardar_contacto, name="guardar_contacto"),
    

    # carrito / checkout
    path("carrito/", views.carrito_view, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("checkout/", views.checkout, name="checkout"),
]


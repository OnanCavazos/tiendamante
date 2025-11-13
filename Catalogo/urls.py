from django.contrib import admin
from django.urls import path
from Catalogo import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),

    # Catálogo
    path("catalogo/", views.catalogo, name="catalogo"),
    path("catalogo/electronica/", views.catalogo_electronica, name="catalogo_electronica"),
    path("catalogo/ropa/", views.catalogo_ropa, name="catalogo_ropa"),
    path("catalogo/electrodomesticos/", views.catalogo_electrodomesticos, name="catalogo_electrodomesticos"),
    path("catalogo/accesorios/", views.catalogo_accesorios, name="catalogo_accesorios"),

    # Carrito
    path("carrito/", views.carrito, name="carrito"),
    path("agregar_al_carrito/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("actualizar_carrito/<int:producto_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("eliminar_del_carrito/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path("procesar_pago/", views.procesar_pago, name="procesar_pago"),

    # Páginas secundarias
    path("acerca/", views.acerca, name="acercade"),
    path("contacto/", views.contacto, name="contacto"),
    path("guardar_contacto/", views.guardar_contacto, name="guardar_contacto"),

    # Autenticación
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),

    path("admin/", admin.site.urls),

    #  Procesar pago
    path("procesar_pago/", views.procesar_pago, name="procesar_pago"),

    # Historial
    path("mis_pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path("pedido/<int:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),


    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),

    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

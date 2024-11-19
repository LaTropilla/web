from django.urls import path
from . import views
from .views import (
    tour_lista, 
    tour_create, 
    tour_update, 
    tour_delete, 
    tour_detalle_pagina, 
    crear_reserva,
    create_preference,
    payment_success,
    payment_failure,
    payment_pending,
    payment_webhook
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Rutas principales
    path('', views.index, name='index'),
    path('paginas/tours/', views.tourshtml, name='tourshtml'),  
    path('paginas/sobrenosotros/', views.sobrenosotroshtml, name='sobrenosotroshtml'), 
    path('paginas/traslados/', views.trasladoshtml, name='trasladoshtml'), 
    
    # APIs
    path('api/tours/', views.tours, name='tours'),
    path('api/filtrotours/', views.filtro_tours, name='filtro_tours'),
    path('api/tourdetalle/<int:tour_id>/', views.tour_detalle, name='tour_detalle'),
    path('api/itinerario/<int:tour_id>/', views.itinerario_api, name='itinerario_api'),
    path('api/crear_reserva', views.crear_reserva, name='crear_reserva'),
    
    # Páginas de tour y reserva
    path('tourdetalle/<int:tour_id>/', tour_detalle_pagina, name='tour_detalle_pagina'),
    path('tureserva', views.confirmar_reserva, name='confirmar_reserva'),
    path('confirmarreserva.html', views.confirmar_reserva, name='confirmar_reserva'),
    
    # Rutas administrativas
    path('admin/tours/', tour_lista, name='tour_lista'),
    path('admin/tours/create/', tour_create, name='tour_create'),
    path('admin/tours/<int:pk>/edit/', tour_update, name='tour_update'),
    path('admin/tours/<int:pk>/delete/', tour_delete, name='tour_delete'),
    
    # Rutas de MercadoPago
    path('payment/create_preference/', create_preference, name='create_preference'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failure/', payment_failure, name='payment_failure'),
    path('payment/pending/', payment_pending, name='payment_pending'),
    path('payment/webhook/', payment_webhook, name='payment_webhook'),
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
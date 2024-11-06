from django.urls import path
from . import views
from .views import tour_lista, tour_create, tour_update, tour_delete, tour_detalle_pagina, crear_reserva
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('paginas/tours/', views.tourshtml, name='tourshtml'),  
    path('paginas/sobrenosotros/', views.sobrenosotroshtml, name='sobrenosotroshtml'), 
    path('paginas/traslados/', views.trasladoshtml, name='trasladoshtml'), 
    path('api/tours/', views.tours, name='tours'),
    path('api/filtrotours/', views.filtro_tours, name='filtro_tours'),
    path('api/tourdetalle/<int:tour_id>/', views.tour_detalle, name='tour_detalle'),
    path('tourdetalle/<int:tour_id>/', tour_detalle_pagina, name='tour_detalle_pagina'),
    path('tureserva', views.confirmar_reserva, name='confirmar_reserva'),
    path('api/crear_reserva', views.crear_reserva, name='crear_reserva'),
    path('confirmarreserva.html', views.confirmar_reserva, name='confirmar_reserva'),
    path('api/itinerario/<int:tour_id>/', views.itinerario_api, name='itinerario_api'),
    path('admin/tours/', tour_lista, name='tour_lista'),
    path('admin/tours/create/', tour_create, name='tour_create'),
    path('admin/tours/<int:pk>/edit/', tour_update, name='tour_update'),
    path('admin/tours/<int:pk>/delete/', tour_delete, name='tour_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
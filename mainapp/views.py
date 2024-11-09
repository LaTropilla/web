from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Tour, TourDetalle, Reserva, Itinerario
from django.contrib.auth.decorators import login_required
from .forms import TourForm
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json



def index(request):
    return render(request, 'index.html')

def tourshtml(request):
    return render(request, 'paginas/tours.html')

def sobrenosotroshtml(request):
    return render(request, 'paginas/sobrenosotros.html')

def trasladoshtml(request):
    return render(request, 'paginas/traslados.html')

def tours(request):
    tours = Tour.objects.all().values()
    return JsonResponse(list(tours), safe=False)

def filtro_tours(request):
    tours = Tour.objects.all()

    tour_desde = request.GET.get('tour_desde')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    dificultad = request.GET.get('dificultad')
    jornada = request.GET.get('jornada')
    precio_maximo = request.GET.get('precio_maximo')

    if tour_desde:
        tours = tours.filter(tour_desde__icontains=tour_desde)
    if desde:
        tours = tours.filter(itinerario__hora_inicio__gte=desde)
    if hasta:
        tours = tours.filter(itinerario__hora_final__lte=hasta)
    if dificultad:
        tours = tours.filter(dificultad__icontains=dificultad)
    if jornada:
        tours = tours.filter(jornada__icontains=jornada)
    if precio_maximo:
        tours = tours.filter(precio__lte=precio_maximo)

    tours = tours.values()

    return JsonResponse(list(tours), safe=False)

def tour_detalle(request, tour_id):
    detalles = get_object_or_404(TourDetalle, tour_id=tour_id)
    response_data = {
        "titulo": detalles.titulo,
        "tipo_actividad": detalles.tipo_actividad,
        "imagen_1": detalles.imagen_1,
        "imagen_2": detalles.imagen_2,
        "imagen_3": detalles.imagen_3,
        "imagen_4": detalles.imagen_4,
        "imagen_5": detalles.imagen_5,
        "imagen_6": detalles.imagen_6,
        "descripcion": detalles.descripcion,
        "url_mapa": detalles.url_mapa
    }
    return JsonResponse(response_data)


def tour_detalle_pagina(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    detalles = get_object_or_404(TourDetalle, tour_id=tour_id)
    context = {
        "titulo": detalles.titulo,
        "tipo_actividad": detalles.tipo_actividad,
        "imagen_1": detalles.imagen_1,
        "descripcion": detalles.descripcion,
        "url_mapa": detalles.url_mapa,
        "dificultad": tour.dificultad,
        "jornada": tour.jornada,
        "ubicacion": tour.ubicacion,
        "precio_adulto": tour.precio,
        "precio_nino": tour.precio_nino,
        "tour_id": tour.id,
        "range": range(1, 7),
        "ruta_carrusel": "/media/tour_detalle/" + str(tour_id) + "/",
    }
    return render(request, 'tourdetalle.html', context)

def itinerario_api(request, tour_id):
    itinerarios = Itinerario.objects.filter(tour_id=tour_id).values('id', 'hora_inicio', 'hora_final', 'actividad', 'detalle_actividad')
    return JsonResponse(list(itinerarios), safe=False)


def confirmar_reserva(request):
    return render(request, 'confirmarreserva.html')

def prueba(request):
    return render(request, 'prueba.html')


@csrf_exempt
def crear_reserva(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reserva = Reserva.objects.create(
            nombre_turista=data['nombre_turista'],
            rut_turista=data['rut_turista'],
            email_turista=data['email_turista'],
            fecha_tour=data['fecha_tour'],
            direccion_recogida=data['direccion_recogida'],
            ciudad_recogida=data['ciudad_recogida'],
            cantidad_adultos=data['cantidad_adultos'],
            cantidad_ninos=data['cantidad_ninos'],
            nombre_tour=data['nombre_tour'],
            precio_total=data['precio_total'],
            fecha_reserva=date.today()
        )
        reserva.save()

        email_subject = '¡Recibimos tu reserva! 🥳 Falta Un Paso Para Confirmar Tu Aventura'
        email_body = f"""
    Hola {reserva.nombre_turista},

    Estamos encantados de que hayas elegido explorar con nosotros y nos aseguraremos de que tengas una experiencia inolvidable. A continuación, te confirmamos los detalles de tu reserva:

        Reserva solicitada para:
         {reserva.nombre_tour}

        Detalles:
        
        🔹Nombre del Turista: {reserva.nombre_turista}
        🔹RUT/Pasaporte: {reserva.rut_turista}
        🔹Email: {reserva.email_turista}

        🔹Fecha del Tour: {reserva.fecha_tour}

        🔹Dirección de Recogida: {reserva.direccion_recogida}
        🔹Ciudad de Recogida: {reserva.ciudad_recogida}

        🔹Cantidad de Adultos: {reserva.cantidad_adultos}
        🔹Cantidad de Niños: {reserva.cantidad_ninos}
        
        🔹Precio Total: {reserva.precio_total}

    ⚠️⚠️ Para finalizar el proceso de reserva, es necesario un último paso ⚠️⚠️ te enviaremos un correo con toda la información. Es muy importante que sigas estas instrucciones para confirmar 
    definitivamente tu participación en el tour.

    Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos. Queremos que te sientas cómod@ y segur@, sabiendo que estamos aquí para ayudarte en cada paso del camino.

    ¡Nos vemos pronto para comenzar esta maravillosa aventura juntos!

    Saludos cordiales,

    Turismo Patagonia Indomia 
        """

        email = EmailMessage(
            email_subject,
            email_body,
            'reservas@profeclauvidelas.cl',
            [reserva.email_turista, 'reservas@profeclauvidelas.cl'],
        )
        email.send(fail_silently=False)

        return JsonResponse({'status': 'Reserva creada'}, status=201)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def tour_lista(request):
    tours = Tour.objects.all()
    return render(request, 'admin/tour_lista.html', {'tours': tours})

@login_required
def tour_create(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tour_lista')
    else:
        form = TourForm()
    return render(request, 'admin/tour_form.html', {'form': form})

@login_required
def tour_update(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_lista')
    else:
        form = TourForm(instance=tour)
    return render(request, 'admin/tour_form.html', {'form': form})

@login_required
def tour_delete(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
        return redirect('tour_lista')
    return render(request, 'admin/tour_eliminar_confirmar.html', {'tour': tour})
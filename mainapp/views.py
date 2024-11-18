from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Tour, TourDetalle, Reserva, Itinerario
from django.contrib.auth.decorators import login_required
from .forms import TourForm
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json
import mercadopago
from django.conf import settings

# Vistas originales
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
            fecha_reserva=date.today(),
            estado_pago='pendiente'
        )
        return JsonResponse({
            'status': 'Reserva creada',
            'reserva_id': reserva.id
        }, status=201)
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

# Funciones auxiliares para MercadoPago
def init_mercadopago():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

def send_confirmation_email(reserva):
    email_subject = '¡Tu reserva ha sido confirmada! 🎉 Prepárate para la aventura'
    email_body = f"""
    ¡Hola {reserva.nombre_turista}!

    ¡Excelentes noticias! Tu pago ha sido confirmado y tu reserva está lista. Aquí están los detalles de tu aventura:

    🎯 Detalles de la Reserva:
    
    Tour: {reserva.nombre_tour}
    Fecha: {reserva.fecha_tour}
    
    📋 Información del Turista:
    Nombre: {reserva.nombre_turista}
    RUT/Pasaporte: {reserva.rut_turista}
    Email: {reserva.email_turista}
    
    📍 Punto de Encuentro:
    Dirección: {reserva.direccion_recogida}
    Ciudad: {reserva.ciudad_recogida}
    
    👥 Participantes:
    Adultos: {reserva.cantidad_adultos}
    Niños: {reserva.cantidad_ninos}
    
    💰 Pago:
    Total pagado: ${reserva.precio_total}
    ID de pago: {reserva.payment_id}
    
    🎉 ¡Todo está listo para tu aventura!
    
    Recomendaciones:
    - Llega 10 minutos antes al punto de encuentro
    - Trae ropa cómoda y apropiada para la actividad
    - No olvides tu cámara para capturar los momentos especiales
    
    Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.
    
    ¡Nos vemos pronto!
    
    Saludos cordiales,
    Turismo "La Tropilla"
    """

    email = EmailMessage(
        email_subject,
        email_body,
        'noreply@turismolatropilla.cl',
        [reserva.email_turista, 'noreply@turismolatropilla.cl'],
    )
    email.send(fail_silently=False)

# Vistas de MercadoPago
@csrf_exempt
def create_preference(request):
    try:
        data = json.loads(request.body)
        reserva_id = data.get('reserva_id')
        reserva = get_object_or_404(Reserva, id=reserva_id)

        preference_data = {
            "items": [
                {
                    "title": f"Reserva Tour - {reserva.nombre_tour}",
                    "quantity": 1,
                    "currency_id": "CLP",
                    "unit_price": float(reserva.precio_total)
                }
            ],
            "back_urls": {
                "success": f"{settings.BASE_URL}/payment/success/",
                "failure": f"{settings.BASE_URL}/payment/failure/",
                "pending": f"{settings.BASE_URL}/payment/pending/"
            },
            "auto_return": "approved",
            "external_reference": str(reserva.id),
            "notification_url": f"{settings.BASE_URL}/payment/webhook/"
        }

        mp = init_mercadopago()
        preference_response = mp.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            reserva.preference_id = preference_response["response"]["id"]
            reserva.save()
            return JsonResponse({
                "id": preference_response["response"]["id"],
                "init_point": preference_response["response"]["init_point"]
            })
        
        return JsonResponse({"error": "Error al crear la preferencia"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    
    reserva = get_object_or_404(Reserva, id=external_reference)
    reserva.estado_pago = 'aprobado'
    reserva.payment_id = payment_id
    reserva.save()
    
    send_confirmation_email(reserva)
    
    return render(request, 'pagos/pago_exitoso.html', {
        'payment_id': payment_id,
        'reserva': reserva
    })

def payment_failure(request):
    external_reference = request.GET.get('external_reference')
    if external_reference:
        reserva = get_object_or_404(Reserva, id=external_reference)
        reserva.estado_pago = 'rechazado'
        reserva.save()
    return render(request, 'pagos/pago_fallido.html')

def payment_pending(request):
    external_reference = request.GET.get('external_reference')
    if external_reference:
        reserva = get_object_or_404(Reserva, id=external_reference)
        reserva.estado_pago = 'pendiente'
        reserva.save()
    return render(request, 'pagos/pago_pendiente.html')

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        try:
            data = request.POST
            if data.get('type') == 'payment':
                payment_id = data.get('data.id')
                mp = init_mercadopago()
                payment_info = mp.payment().get(payment_id)
                
                if payment_info["status"] == 200:
                    payment_data = payment_info["response"]
                    reserva = Reserva.objects.get(id=payment_data["external_reference"])
                    
                    if payment_data["status"] == "approved":
                        reserva.estado_pago = 'aprobado'
                        reserva.payment_id = payment_id
                        reserva.save()
                        send_confirmation_email(reserva)
                    elif payment_data["status"] == "rejected":
                        reserva.estado_pago = 'rechazado'
                        reserva.save()
                    
                    return JsonResponse({"status": "success"})
            
            return JsonResponse({"status": "ignored"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)
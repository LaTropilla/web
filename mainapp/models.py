from django.db import models
from datetime import date

class Tour(models.Model):
    DIFICULTAD_OPCIONES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    JORNADA_OPCIONES = [
        ('Medio día', 'Medio día'),
        ('Día Completo', 'Día Completo'),
    ]

    UBICACION_OPCIONES = [
        ('Parque Nacional Torres del Paine', 'Parque Nacional Torres del Paine'),
        ('Punta Arenas', 'Punta Arenas'),
        ('Puerto Natales', 'Puerto Natales'),
    ]

    TIEMPO_OPCIONES = [
        ('1 hora', '1 hora'),
        ('2 horas', '2 horas'),
        ('3 horas', '3 horas'),
        ('4 horas', '4 horas'),
        ('5 horas', '5 horas'),
        ('6 horas', '6 horas'),
        ('7 horas', '7 horas'),
        ('8 horas', '8 horas'),
        ('9 horas', '9 horas'),
        ('10 horas', '10 horas'),
        ('11 horas', '11 horas'),
        ('12 horas', '12 horas'),
        ('13 horas', '13 horas'),
        ('14 horas', '14 horas'),
        ('15 horas', '15 horas')
    ]

    DESDE_OPCIONES = [
        ('Parque Nacional Torres del Paine', 'Parque Nacional Torres del Paine'),
        ('Punta Arenas', 'Punta Arenas'),
        ('Puerto Natales', 'Puerto Natales'),
        ('Punta Arenas, Puerto Natales', 'Punta Arenas, Puerto Natales'),
        ('Parque Nacional Torres del Paine, Punta Arenas', 'Parque Nacional Torres del Paine, Punta Arenas'),
        ('Parque Nacional Torres del Paine, Puerto Natales', 'Parque Nacional Torres del Paine, Puerto Natales'),        
        ('Parque Nacional Torres del Paine, Punta Arenas, Puerto Natales', 'Parque Nacional Torres del Paine, Punta Arenas, Puerto Natales'),   
    ]


    nombre = models.CharField(max_length=255)
    tiempo = models.CharField(max_length=255, choices= TIEMPO_OPCIONES)
    ubicacion = models.CharField(max_length=255, choices=UBICACION_OPCIONES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nino = models.DecimalField(max_digits=10, decimal_places=2)
    dificultad = models.CharField(max_length=5, choices=DIFICULTAD_OPCIONES)
    jornada = models.CharField(max_length=255, choices=JORNADA_OPCIONES)
    imagen = models.ImageField(upload_to='tours/images/')
    tour_desde = models.CharField(max_length=255, choices=DESDE_OPCIONES)
    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    def __str__(self):
        return self.nombre


class Itinerario(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    actividad = models.CharField(max_length=255)
    detalle_actividad = models.TextField()

    def __str__(self):
        return f'{self.actividad} ({self.hora_inicio} - {self.hora_final})'

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_turista = models.CharField(max_length=255)
    rut_turista = models.CharField(max_length=12)
    email_turista = models.EmailField(default="ejemplo@ejemplo.cl")  
    fecha_tour = models.DateField()
    fecha_reserva = models.DateField(default=date.today)
    direccion_recogida = models.CharField(max_length=255)
    ciudad_recogida = models.CharField(max_length=255)
    cantidad_adultos = models.IntegerField()
    cantidad_ninos = models.IntegerField()
    nombre_tour = models.CharField(max_length=255, default="tournombre")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_turista} - {self.nombre_tour} ({self.fecha_tour})"

class TourDetalle(models.Model):
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE)
    titulo = models.TextField()
    tipo_actividad = models.TextField()
    imagen_1 = models.ImageField(upload_to='tour_detalle')
    imagen_2 = models.ImageField(upload_to='tour_detalle')
    imagen_3 = models.ImageField(upload_to='tour_detalle')
    imagen_4 = models.ImageField(upload_to='tour_detalle')
    imagen_5 = models.ImageField(upload_to='tour_detalle')
    imagen_6 = models.ImageField(upload_to='tour_detalle')
    descripcion = models.TextField()
    url_mapa = models.CharField(max_length=600)

    def __str__(self):
        return f"Detalles {self.tour.nombre}"


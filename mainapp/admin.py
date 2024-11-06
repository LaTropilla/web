from django.contrib import admin, messages
from django import forms
from django.forms import ModelForm, TimeInput
from .models import Tour, Reserva, TourDetalle, Itinerario

class TourDetalleForm(forms.ModelForm):
    class Meta:
        model = TourDetalle
        fields = ['titulo', 'tipo_actividad', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'imagen_6', 'descripcion', 'url_mapa']

class TourDetalleInline(admin.StackedInline):
    model = TourDetalle
    form = TourDetalleForm
    can_delete = False
    verbose_name_plural = 'Detalles del Tour'

class ItinerarioForm(ModelForm):
    class Meta:
        model = Itinerario
        fields = ['hora_inicio', 'hora_final', 'actividad', 'detalle_actividad']
        widgets = {
            'hora_inicio': TimeInput(format='%H:%M'),
            'hora_final': TimeInput(format='%H:%M'),
        }

class ItinerarioInline(admin.TabularInline):
    model = Itinerario
    extra = 1  # Cuántos itinerarios se mostrarán para agregar

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourDetalleInline, ItinerarioInline]
    list_display = ('nombre', 'precio', 'dificultad', 'jornada', 'ubicacion')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('dificultad', 'jornada', 'ubicacion')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'tourdetalle'):
            TourDetalle.objects.create(tour=obj)

        itinerarios = Itinerario.objects.filter(tour=obj)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('fecha_tour', 'nombre_tour', 'direccion_recogida', 'ciudad_recogida', 'cantidad_adultos', 'cantidad_ninos', 'precio_total', 'nombre_turista', 'rut_turista', 'email_turista', 'fecha_reserva')
    list_filter = ('fecha_tour', 'ciudad_recogida')
    search_fields = ('nombre_turista', 'rut_turista', 'email_turista', 'nombre_tour')


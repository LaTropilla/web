from django import forms
from .models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['nombre', 'tiempo', 'ubicacion', 'precio', 'precio_nino', 'dificultad', 'jornada', 'imagen', 'tour_desde']

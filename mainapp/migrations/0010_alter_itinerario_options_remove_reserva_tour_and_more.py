# Generated by Django 5.0.7 on 2024-07-23 05:23

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_remove_tourdetalle_extensionimagenes_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itinerario',
            options={},
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='tourdetalle',
            name='extensionimagenes',
        ),
        migrations.RemoveField(
            model_name='tourdetalle',
            name='nombre_base_imagen',
        ),
        migrations.AddField(
            model_name='reserva',
            name='fecha_reserva',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='reserva',
            name='nombre_tour',
            field=models.CharField(default='tournombre', max_length=255),
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_1',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_2',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_3',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_4',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_5',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tourdetalle',
            name='imagen_6',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='tour_detalle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itinerario',
            name='actividad',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='ciudad_recogida',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='direccion_recogida',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tour',
            name='dificultad',
            field=models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], max_length=5),
        ),
        migrations.AlterField(
            model_name='tour',
            name='jornada',
            field=models.CharField(choices=[('Medio día', 'Medio día'), ('Día Completo', 'Día Completo')], max_length=255),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tiempo',
            field=models.CharField(choices=[('1 hora', '1 hora'), ('2 horas', '2 horas'), ('3 horas', '3 horas'), ('4 horas', '4 horas'), ('5 horas', '5 horas'), ('6 horas', '6 horas'), ('7 horas', '7 horas'), ('8 horas', '8 horas'), ('9 horas', '9 horas'), ('10 horas', '10 horas'), ('11 horas', '11 horas'), ('12 horas', '12 horas'), ('13 horas', '13 horas'), ('14 horas', '14 horas'), ('15 horas', '15 horas')], max_length=255),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_desde',
            field=models.CharField(choices=[('Parque Nacional Torres del Paine', 'Parque Nacional Torres del Paine'), ('Punta Arenas', 'Punta Arenas'), ('Puerto Natales', 'Puerto Natales'), ('Punta Arenas, Puerto Natales', 'Punta Arenas, Puerto Natales'), ('Parque Nacional Torres del Paine, Punta Arenas', 'Parque Nacional Torres del Paine, Punta Arenas'), ('Parque Nacional Torres del Paine, Puerto Natales', 'Parque Nacional Torres del Paine, Puerto Natales'), ('Parque Nacional Torres del Paine, Punta Arenas, Puerto Natales', 'Parque Nacional Torres del Paine, Punta Arenas, Puerto Natales')], max_length=255),
        ),
        migrations.AlterField(
            model_name='tour',
            name='ubicacion',
            field=models.CharField(choices=[('Parque Nacional Torres del Paine', 'Parque Nacional Torres del Paine'), ('Punta Arenas', 'Punta Arenas'), ('Puerto Natales', 'Puerto Natales')], max_length=255),
        ),
    ]

import os
import django
from django.db import connection
from django.db.utils import OperationalError

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pindomia.settings')
django.setup()

def test_database_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            print('Conexión exitosa a la base de datos')
    except OperationalError as e:
        print(f'Error de conexión a la base de datos: {e}')

if __name__ == '__main__':
    test_database_connection()

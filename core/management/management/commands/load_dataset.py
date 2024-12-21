# myapp/management/commands/load_large_dataset.py
import csv  # o la librería que necesites (puede ser pandas, openpyxl, etc.)
from django.core.management.base import BaseCommand, CommandError
from myapp.models import TuModelo  # Ajusta según tu modelo

class Command(BaseCommand):
    help = "Carga un gran conjunto de datos en la base de datos."

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Ruta del archivo que contiene los datos a importar.'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not file_path:
            raise CommandError('Debes proporcionar la ruta del archivo con --file=...')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Aquí un ejemplo para CSV, ajusta si necesitas JSON, Excel, etc.
                reader = csv.DictReader(f)
                for row in reader:
                    # Suponiendo que tus columnas del CSV se llaman "campo1", "campo2", etc.
                    TuModelo.objects.create(
                        campo1=row['campo1'],
                        campo2=row['campo2'],
                        # ...
                    )
            self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente.'))
        except Exception as e:
            raise CommandError(f'Error cargando el archivo: {e}')

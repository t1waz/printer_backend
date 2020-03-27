import os


IMAGE_DIR = '/files'

PRINTER_HOST = os.getenv('PRINTER_HOST')

PRINTER_USER = os.getenv('PRINTER_USER')

HOST_APP_DIR = os.getenv('HOST_APP_DIR')

APP_CONFIG = {}

MAIN_PIPELINE = [
    'services.ImageService',
    'services.PrinterService',
]

DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('POSTGRES_HOST'),
                'port': os.getenv('POSTGRES_PORT'),
                'user': os.getenv('POSTGRES_USER'),
                'password': os.getenv('POSTGRES_PASSWORD'),
                'database': os.getenv('POSTGRES_NAME'),
            }
        },
    },
    'apps': {
        'models': {
            'models': ['models'],
        }
    }
}

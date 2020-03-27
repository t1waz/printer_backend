import asyncio
import time
from io import BytesIO

from PIL import Image

import settings
from constants import FileStatus
from models import File
import asyncssh


class SSHService:
    @classmethod
    async def execute_command(cls, command):
        async with asyncssh.connect(host=settings.PRINTER_HOST,
                                    username=settings.PRINTER_USER,
                                    client_keys=['/run/secrets/rsa']) as connection:
            data = await connection.run(command, check=True)

            return data.stdout


class FileService:
    @classmethod
    async def create_file(cls, data):
        try:
            return await File.create(name=f'{int(time.time())}.png',
                                     data=data,
                                     status=FileStatus.REGISTER)
        except TypeError:
            return None


class ImageService:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    @staticmethod
    def get_image_from_input_bytes(input_bytes, mode='RGB'):
        if mode not in ('RGB',):
            return None, 'invalid mode'

        try:
            stream = BytesIO(input_bytes)
        except TypeError:
            return None, 'incorrect input bytes'

        try:
            return Image.open(stream).convert(mode), None
        except (TypeError, ValueError):
            return None, 'cannot create image'

    @staticmethod
    def save_image(image=None, filename='', path=settings.IMAGE_DIR):
        if not filename:
            return None, 'filename cannot be empty'
        if not isinstance(image, Image.Image):
            return None, 'image must be PIL image instance'
        elif not isinstance(filename, str) or not isinstance(path, str):
            return None, 'filename and path must be a string'

        if not path or path == '.':
            image_path = f'{filename}'
        else:
            image_path = f'{path}/{filename}'

        image.save(image_path, format='png')

        return image_path, None

    async def start(self):
        while True:
            file = await self.input_queue.get()
            if file:
                loop = asyncio.get_event_loop()
                image, error = await loop.run_in_executor(None,
                                                          self.get_image_from_input_bytes,
                                                          file.data)
                if not image:
                    file.status = FileStatus.ERROR
                    await file.save()

                success, error = await loop.run_in_executor(None,
                                                            self.save_image,
                                                            image,
                                                            file.name)

                if not success:
                    file.status = FileStatus.ERROR
                    await file.save()

                file.status = FileStatus.IMAGE_CREATED
                await self.output_queue.put(file)


class PrinterService:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    async def start(self):
        while True:
            file = await self.input_queue.get()
            if file:
                data = await SSHService.execute_command(f'lp -d dymo {settings.HOST_APP_DIR}'
                                                        f'/files/{file.name} -o '
                                                        f'media=Custom.102x256')

from tortoise import fields
from tortoise.models import Model

from constants import FileStatus


class File(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    data = fields.BinaryField()
    status = fields.IntEnumField(FileStatus)

    def __str__(self):
        return f'id: {self.id} url:{self.name}'

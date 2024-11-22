import datetime
from django.db import models, transaction


class IDGenerator(models.Model):
    date = models.CharField(max_length=8, unique=True)
    sequence = models.IntegerField(default=0)


def generate_custom_id():
    today = datetime.datetime.now().strftime("%Y%m%d")

    with transaction.atomic():
        id_gen, created = IDGenerator.objects.get_or_create(date=today)
        id_gen.sequence += 1
        id_gen.save()

    custom_id = f"TC{today}{id_gen.sequence:04d}"
    return custom_id

from django.db import models

import uuid

from clickhouse_backend import models as ch
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Factory(models.Model):
    """ЗМК"""

    external_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FactoryUser(models.Model):
    """Пользователь завода"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)



class WorkVolume(models.Model):
    """Объем работы"""

    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    start = models.DateField()
    finish = models.DateField()
    weight = models.PositiveIntegerField()
    created = models.DateField(default=timezone.localdate)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["factory", "start", "finish"],
                name="unique_work_volume_period",
            )
        ]


def next_record_id():
    """счетчик для ClickHouse"""
    last = WorkVolumeRecord.objects.aggregate(m=models.Max("id"))["m"]
    return (last or 0) + 1

class WorkVolumeRecord(ch.ClickhouseModel):
    """Запись объема работы"""

    id = ch.UInt32Field(primary_key=True, default=next_record_id)
    factory = ch.UUIDField()      # Factory.external_id
    start = ch.DateField()
    finish = ch.DateField()
    weight = ch.UInt32Field()
    author = ch.UInt32Field()     # User.pk
    created = ch.DateField(default=timezone.localdate)

    class Meta:
        engine = ch.MergeTree(order_by=("id",))
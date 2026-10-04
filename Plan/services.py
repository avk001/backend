from django.contrib.auth.models import User
from django.utils import timezone

from .models import Factory, FactoryUser, WorkVolume, WorkVolumeRecord

GROUP_FACTORY_REP = "Представитель ЗМК"
GROUP_MANAGER = "Менеджер по взаимодействию с ЗМК"


class FactoryNotFound(Exception):
    """ЗМК не существует"""



class AccessDenied(Exception):
    """Пользователь не найден или не в группе"""


def save_work_volume(*, factory_id, start, finish, weight, author_id):

    # проверка ЗМК
    factory = Factory.objects.filter(pk=factory_id).first()
    if factory is None:
        raise FactoryNotFound

    # проверка пользователя
    author = User.objects.filter(pk=author_id).first()
    if author is None:
        raise AccessDenied

    groups = set(author.groups.values_list("name", flat=True))
    if GROUP_FACTORY_REP in groups:
        if not FactoryUser.objects.filter(user=author, factory=factory).exists():
            raise FactoryNotFound
    elif GROUP_MANAGER not in groups:
        raise AccessDenied

    today = timezone.localdate()

    # Postgres create or update
    WorkVolume.objects.update_or_create(
        factory=factory,
        start=start,
        finish=finish,
        defaults={"weight": weight, "created": today},
    )

    # ClickHouse add item
    WorkVolumeRecord.objects.create(
        factory=factory.external_id,
        start=start,
        finish=finish,
        weight=weight,
        author=author.pk,
        created=today,
    )
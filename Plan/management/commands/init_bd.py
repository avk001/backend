from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from Plan.models import Factory, FactoryUser
from Plan.services import GROUP_FACTORY_REP, GROUP_MANAGER


class Command(BaseCommand):
    help = "Создает тестовые данные: группы, два ЗМК и трех пользователей"

    def handle(self, *args, **options):
        rep_group, _ = Group.objects.get_or_create(name=GROUP_FACTORY_REP)
        manager_group, _ = Group.objects.get_or_create(name=GROUP_MANAGER)

        # создаем ЗМК
        factory1, _ = Factory.objects.get_or_create(name="ЗМК 1")
        factory2, _ = Factory.objects.get_or_create(name="ЗМК 2")

        # create users
        rep, _ = User.objects.get_or_create(username="rep1")
        manager, _ = User.objects.get_or_create(username="manager1")
        guest, _ = User.objects.get_or_create(username="guest1")

        rep.groups.add(rep_group)
        manager.groups.add(manager_group)
        FactoryUser.objects.get_or_create(user=rep, factory=factory1)

        self.stdout.write(f"{factory1.name}: id={factory1.pk}")
        self.stdout.write(f"{factory2.name}: id={factory2.pk}")
        self.stdout.write(f"rep1 (представитель {factory1.name}): id={rep.pk}")
        self.stdout.write(f"manager1 (менеджер): id={manager.pk}")
        self.stdout.write(f"guest1 (без группы): id={guest.pk}")

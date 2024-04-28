from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from studying.models import Lesson, Course


content_type_1 = ContentType.objects.get_for_model(Lesson)
sending_permissions = [
    'view_lesson',
    'update_lesson',
]
content_type_2 = ContentType.objects.get_for_model(Course)
user_permissions = [
    'view_course',
    'update_course',
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        managers_group = Group.objects.create(name='managers')
        for p in sending_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_1)
            managers_group.permissions.add(perm)
        for p in user_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_2)
            managers_group.permissions.add(perm)
        managers_group.save()

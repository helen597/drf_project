from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from studying.models import Lesson, Course


content_type_1 = ContentType.objects.get_for_model(Lesson)
lesson_permissions = [
    'view_lesson',
    'change_lesson'
]
content_type_2 = ContentType.objects.get_for_model(Course)
course_permissions = [
    'view_course',
    'change_course'
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        managers_group = Group.objects.create(name='managers')
        for p in lesson_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_1)
            managers_group.permissions.add(perm)
        for p in course_permissions:
            perm = Permission.objects.get(codename=p, content_type=content_type_2)
            managers_group.permissions.add(perm)
        managers_group.save()

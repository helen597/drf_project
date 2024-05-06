from rest_framework.test import APITestCase
from users.models import User
from studying.models import Course, Lesson
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="helen597@yandex.ru")
        self.course = Course.objects.create(title="English")
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('studying:lessons-get', args=(self.lesson.pk, ))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse('studying:lessons-create')
        data = {
            'title': 'Lesson 2',
            'course': self.course
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('studying:lessons-update', args=(self.lesson.pk, ))
        data = {
            'title': 'Lesson 1. Present Simple'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), 'Lesson 1. Present Simple')


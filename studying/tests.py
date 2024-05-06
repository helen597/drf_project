from rest_framework.test import APITestCase
from users.models import User
from studying.models import Course, Lesson, Subscription
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="helen597@yandex.ru")
        self.user.set_password('59hl71ee')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="English", owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, owner=self.user)

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
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('studying:lessons-update', args=(self.lesson.pk, ))
        data = {
            'title': 'Lesson 1. Present Simple'
        }
        response = self.client.patch(url, data)
        data = response.json()
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), 'Lesson 1. Present Simple')

    def test_lesson_delete(self):
        url = reverse('studying:lessons-delete', args=(self.lesson.pk, ))
        response = self.client.delete(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('studying:lessons-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)

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
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, owner=self.user,
                                            video_link='youtube.com/ghfjgbkjbg')

    def test_lesson_retrieve(self):
        url = reverse('studying:lessons-get', args=(self.lesson.pk,))
        response = self.client.get(url)
        print('\ntest_lesson_retrieve')
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse('studying:lessons-create')
        data = {
            'title': 'Lesson 2',
            'course': self.course.pk,
            'owner': self.user.pk,
            'video_link': 'youtube.com/ghfjgbkjbg'
        }
        response = self.client.post(url, data)
        print('\ntest_lesson_create')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('studying:lessons-update', args=(self.lesson.pk,))
        data = {
            'title': 'Lesson 1. Present Simple',
            'video_link': 'youtube.com/ghfjgbkjbg'
        }
        response = self.client.patch(url, data)
        data = response.json()
        print('\ntest_lesson_update')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), 'Lesson 1. Present Simple')

    def test_lesson_delete(self):
        url = reverse('studying:lessons-delete', args=(self.lesson.pk,))
        # self.lesson.owner = self.user
        response = self.client.delete(url)
        print('\ntest_lesson_delete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('studying:lessons-list')
        response = self.client.get(url)
        print('\ntest_lesson_list')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="helen597@yandex.ru")
        self.user.set_password('59hl71ee')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="English", owner=self.user)

    def test_subscribe(self):
        url = reverse('studying:subscribe', args=(self.course.pk,))
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Подписка добавлена'})

    def test_unsubscribe(self):
        url = reverse('studying:subscribe', args=(self.course.pk,))
        Subscription.objects.create(course=self.course, user=self.user)
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Подписка удалена'})

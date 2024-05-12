from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение', **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')
    video_link = models.CharField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)
    price = models.PositiveIntegerField(default=50000, verbose_name='стоимость курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('title',)


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='lessons/', verbose_name='Изображение', **NULLABLE)
    video_link = models.CharField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')
    price = models.PositiveIntegerField(default=1000, verbose_name='стоимость урока')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('title',)


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'Подписка на курс {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

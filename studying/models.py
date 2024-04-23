from django.db import models
NULLABLE = {'null': True, 'blank': True}

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение', **NULLABLE)

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
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('title',)

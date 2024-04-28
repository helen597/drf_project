from django.db import models
from django.contrib.auth.models import AbstractUser
from studying.models import NULLABLE, Lesson, Course


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Telegram_id', **NULLABLE )
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    verification_code = models.CharField(max_length=10, verbose_name='код верификации', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('email',)
        

class Payment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='', **NULLABLE)
    deposit = models.IntegerField(verbose_name='')
    method_choices = {"наличными": "наличными", "переводом": "переводом"}
    method = models.CharField(max_length=9, choices=method_choices, verbose_name='')

    def __str__(self):
        return (f'{self.date} - {self.deposit} рублей {self.method} от {self.user} '
                f'за {self.paid_course if self.paid_course else self.paid_lesson}')

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'

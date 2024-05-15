from django.db import models
from django.contrib.auth.models import AbstractUser
from studying.models import NULLABLE, Lesson, Course


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Telegram_id', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    verification_code = models.CharField(max_length=10, verbose_name='код верификации', **NULLABLE)
    last_login = models.DateTimeField(**NULLABLE, verbose_name='дата последнего входа')
    is_active = models.BooleanField(default=False, verbose_name='активен')
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
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата платежа')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма')
    method_choices = {"наличными": "наличными", "переводом": "переводом"}
    method = models.CharField(max_length=9, choices=method_choices, verbose_name='способ оплаты')
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name='ID сессии')
    link = models.URLField(max_length=400, **NULLABLE, verbose_name='ссылка на оплату')

    def __str__(self):
        return (f'{self.date} - {self.amount} рублей {self.method} от {self.user} '
                f'за {self.paid_course if self.paid_course else self.paid_lesson}')

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'

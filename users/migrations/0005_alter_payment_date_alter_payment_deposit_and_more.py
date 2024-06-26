# Generated by Django 5.0.4 on 2024-05-07 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studying', '0005_course_price_lesson_price'),
        ('users', '0004_user_telegram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата платежа'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='deposit',
            field=models.IntegerField(verbose_name='сумма'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studying.course', verbose_name='оплаченный курс'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paid_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studying.lesson', verbose_name='оплаченный урок'),
        ),
    ]

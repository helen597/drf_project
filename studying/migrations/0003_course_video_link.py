# Generated by Django 5.0.4 on 2024-05-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studying', '0002_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_link',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ссылка на видео'),
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payment_date_alter_payment_deposit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='deposit',
            field=models.PositiveIntegerField(verbose_name='сумма'),
        ),
    ]

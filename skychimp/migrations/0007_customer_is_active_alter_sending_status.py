# Generated by Django 4.2.2 on 2023-07-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skychimp', '0006_sending_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активный'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='status',
            field=models.CharField(choices=[('Создана', 'Создана'), ('Завершена', 'Завершена'), ('Запущена', 'Запущена')], default='Создана', max_length=50, verbose_name='Статус'),
        ),
    ]
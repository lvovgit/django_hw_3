# Generated by Django 4.2.2 on 2023-06-27 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Создатель'),
        ),
    ]
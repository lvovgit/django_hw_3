# Generated by Django 4.2.2 on 2023-07-02 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skychimp', '0002_message_alter_customer_options_sending_attempt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attempt',
            options={'verbose_name': 'Статистика (попытка)', 'verbose_name_plural': 'Статистики (попытки)'},
        ),
        migrations.AlterModelOptions(
            name='sending',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='broadcast',
        ),
        migrations.AddField(
            model_name='attempt',
            name='sending',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='skychimp.sending', verbose_name='Рассылка'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='response',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ сервера'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='status',
            field=models.CharField(choices=[('в процессе', 'В процессе'), ('успешно', 'Успешно'), ('не удачно', 'Не удачно')], max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='message',
            field=models.TextField(verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=254, verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='frequency',
            field=models.CharField(choices=[('1 раз в день', '1 раз в день'), ('1 раз в неделю', '1 раз в неделю'), ('1 раз в месяц', '1 раз в месяц')], max_length=14, verbose_name='Периодичность'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skychimp.message', verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='status',
            field=models.CharField(choices=[('создана', 'Создана'), ('завершена', 'Завершена'), ('запущена', 'Запущена')], default='created', max_length=50, verbose_name='Статус'),
        ),
    ]
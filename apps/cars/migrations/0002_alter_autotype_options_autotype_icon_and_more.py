# Generated by Django 4.0.5 on 2022-06-19 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autotype',
            options={'verbose_name': 'Тип', 'verbose_name_plural': 'Типы'},
        ),
        migrations.AddField(
            model_name='autotype',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='type_icon/'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='type_auto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.autotype', verbose_name='тип'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]

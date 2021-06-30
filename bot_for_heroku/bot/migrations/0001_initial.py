# Generated by Django 3.2.4 on 2021-06-30 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('p_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='ФИО')),
                ('telephone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('oblast', models.CharField(max_length=50, null=True, verbose_name='Область')),
                ('raion', models.CharField(max_length=200, null=True, verbose_name='Район')),
                ('doljnost', models.CharField(max_length=50, null=True, verbose_name='Должность')),
                ('sale', models.BooleanField(default=False, verbose_name='Подтвержден админом')),
                ('city', models.CharField(max_length=50, null=True, verbose_name='Город')),
                ('kenesh', models.CharField(max_length=50, null=True, verbose_name='Кенеш')),
            ],
            options={
                'verbose_name': 'Люди',
                'verbose_name_plural': 'Люди',
            },
        ),
    ]

# Generated by Django 4.2 on 2023-04-28 12:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_applying_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applying',
            name='priority',
            field=models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]

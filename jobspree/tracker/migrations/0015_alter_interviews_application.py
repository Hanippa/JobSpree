# Generated by Django 4.2 on 2023-05-09 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_interviews_suggestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviews',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.applied'),
        ),
    ]

# Generated by Django 4.2 on 2023-05-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0013_interviews_transcript_alter_applied_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviews',
            name='suggestions',
            field=models.TextField(blank=True, null=True),
        ),
    ]

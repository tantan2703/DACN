# Generated by Django 4.2.7 on 2024-01-16 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_row__processing_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='row',
            name='_processing_seats',
        ),
    ]

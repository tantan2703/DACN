# Generated by Django 4.2.7 on 2024-01-15 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_seat_concert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('seats_per_row', models.IntegerField(default=20)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='booking.concert')),
            ],
        ),
    ]

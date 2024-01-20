# Generated by Django 4.2.7 on 2024-01-20 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]

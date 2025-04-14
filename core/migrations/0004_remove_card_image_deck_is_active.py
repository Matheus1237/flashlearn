# Generated by Django 4.0 on 2025-04-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_card_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='image',
        ),
        migrations.AddField(
            model_name='deck',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

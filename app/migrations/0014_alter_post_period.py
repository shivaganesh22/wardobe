# Generated by Django 5.1.3 on 2025-01-06 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_order_delivery_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='period',
            field=models.DateField(default=datetime.date(2026, 1, 6)),
        ),
    ]

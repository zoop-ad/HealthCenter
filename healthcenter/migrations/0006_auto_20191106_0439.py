# Generated by Django 2.2.6 on 2019-11-06 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcenter', '0005_auto_20191106_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opdregistration',
            name='checkup_time',
            field=models.TimeField(default=datetime.datetime(2019, 11, 6, 4, 39, 14, 393373)),
        ),
    ]

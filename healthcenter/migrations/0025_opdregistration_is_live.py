# Generated by Django 2.2.10 on 2020-05-19 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcenter', '0024_auto_20200512_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='opdregistration',
            name='is_live',
            field=models.BooleanField(default=False),
        ),
    ]

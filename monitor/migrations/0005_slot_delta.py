# Generated by Django 2.1.4 on 2019-02-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20190220_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='delta',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
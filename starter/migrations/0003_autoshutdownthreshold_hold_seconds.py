# Generated by Django 2.1.4 on 2019-02-21 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starter', '0002_autoshutdownthreshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoshutdownthreshold',
            name='hold_seconds',
            field=models.IntegerField(default=1800),
        ),
    ]

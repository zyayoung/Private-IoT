# Generated by Django 2.1.4 on 2019-02-19 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='data',
            new_name='value',
        ),
    ]

# Generated by Django 3.2.5 on 2021-09-23 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_cubedots', '0025_auto_20210923_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='manager',
        ),
        migrations.RemoveField(
            model_name='teamleader',
            name='tl',
        ),
    ]

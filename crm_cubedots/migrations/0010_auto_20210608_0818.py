# Generated by Django 3.1.7 on 2021-06-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_cubedots', '0009_auto_20210608_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task_duration',
            field=models.BigIntegerField(default=0),
        ),
    ]

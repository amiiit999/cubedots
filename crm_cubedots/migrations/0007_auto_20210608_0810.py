# Generated by Django 3.1.7 on 2021-06-08 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_cubedots', '0006_auto_20210608_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pretasks',
            name='required_time',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_duration',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]

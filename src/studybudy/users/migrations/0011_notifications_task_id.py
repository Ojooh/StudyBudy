# Generated by Django 3.0.5 on 2020-08-31 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='task_id',
            field=models.BigIntegerField(default=0),
        ),
    ]

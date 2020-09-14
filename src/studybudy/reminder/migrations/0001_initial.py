# Generated by Django 3.0.5 on 2020-08-27 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('task', models.CharField(max_length=150)),
                ('time', models.DateTimeField()),
                ('time_zone', timezone_field.fields.TimeZoneField(default='UTC')),
                ('task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('passed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

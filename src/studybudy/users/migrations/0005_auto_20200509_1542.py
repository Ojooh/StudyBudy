# Generated by Django 3.0.5 on 2020-05-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200507_0212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstate',
            old_name='order',
            new_name='file_order',
        ),
        migrations.AddField(
            model_name='userstate',
            name='folder_order',
            field=models.CharField(default='ASC', max_length=100),
        ),
    ]

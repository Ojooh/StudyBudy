import random, os
from django.db import models
from users.models import User
# from django.utils.six import python_2_unicode_compatible
from timezone_field import TimeZoneField




# Create your models here.
# @python_2_unicode_compatible
class TaskReminder(models.Model):
    user                = models.ForeignKey(User, related_name="task_creator", on_delete=models.CASCADE, blank=True, null=True,)
    phone_number        = models.CharField(max_length=15)
    task                = models.CharField(max_length=150)
    time                = models.DateTimeField(blank=True, null=True)
    time_zone           = TimeZoneField(default='UTC')
    task_id             = models.CharField(max_length=50, blank=True, editable=False)
    created             = models.DateTimeField(auto_now_add=True)
    completed           = models.BooleanField(default=False)
    passed              = models.BooleanField(default=False)

    def __str__(self):
        return 'Reminder {0} - {1}'.format(self.pk, self.user.last_name)


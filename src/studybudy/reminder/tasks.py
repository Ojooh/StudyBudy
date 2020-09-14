from celery.task.schedules import crontab
from celery.decorators import task
from celery.utils.log import get_task_logger
from .models import TaskReminder
from django.core.mail import send_mail

logger = get_task_logger(__name__)



@task(name="send_email_reminder")
def send_email_reminder(appointment_id, from_email):
    """Send a reminder via email """
    # Get our appointment from the database
    try:
        appointment = TaskReminder.objects.get(pk=appointment_id)
    except TaskReminder.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return


    if appointment.completed is False:
        appointment_time        = arrow.get(appointment.time, appointment.time_zone.zone)
        body                    = 'Hi {0}. You have an appointment coming up at {1}.'.format( appointment.user.last_name, appointment_time.format('h:mm a'))
        to_email                = appointment.user.email

        print(body)

        send_mail("Task Reminder", body, from_email, to_email, **kwargs)
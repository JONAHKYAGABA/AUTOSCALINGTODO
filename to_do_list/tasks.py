from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from calendarapp.models import Event

@shared_task
def send_notification(event_id):
    event = Event.objects.get(id=event_id)
    user_email = event.user.email
    event_title = event.title
    event_start_time = event.start_time
    event_end_time = event.end_time
    start_reminder_datetime = event_start_time - timedelta(minutes=30)
    end_reminder_datetime = event_end_time - timedelta(minutes=30)
    
    send_mail(
        'Event Reminder',
        f'Your event "{event_title}" is starting in 30 minutes at {event_start_time.strftime("%Y-%m-%d %H:%M")} and ending in 30 minutes at {event_end_time.strftime("%Y-%m-%d %H:%M")}.',
        settings.EMAIL_HOST_USER,
        ['user_email'],
        fail_silently=False,
    )

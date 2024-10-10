from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail



# Create your models here.
class Task(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=200)
    description=models.CharField(null=True,blank=True,max_length=200)
    complete = models.BooleanField(default=False)
    due  = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    time=models.TimeField( auto_now_add=False,auto_now=False,blank=True,null=True)
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering =['complete']
    
    
class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f'Reminder for {self.task.title} at {self.reminder_date}'
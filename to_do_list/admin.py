from django.contrib import admin
from . models import Task ,Reminder

# Register your models here.
admin.site.register(Task)
admin.site.register(Reminder)
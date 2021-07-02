from django.contrib import admin

from .models import Job, Column

# Register your models here.
admin.site.register(Job)
admin.site.register(Column)
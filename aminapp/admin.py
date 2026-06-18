from django.contrib import admin
from .models import signup, ActiveSession, Feedback

admin.site.register(signup)
admin.site.register(ActiveSession)
admin.site.register(Feedback)
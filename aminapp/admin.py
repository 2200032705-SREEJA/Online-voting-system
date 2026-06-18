from django.contrib import admin
from aminapp.models import signup, ActiveSession, Feedback, Candidate, Vote

admin.site.register(signup)
admin.site.register(ActiveSession)
admin.site.register(Feedback)
admin.site.register(Candidate)
admin.site.register(Vote)
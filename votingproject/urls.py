from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('amin/', admin.site.urls),
    path("demo", views.demofunctio, name="demo"),
    path("", views.welcome, name="root"),          # ← CHANGED: was views.login
    path("welcome", views.welcome, name="welcome"), # ← NEW
    path("home", views.homefunction, name="home"),
    path("voterregistration", views.voterregistratiofunction, name="voterregistration"),
    path('createregister/', views.createregister, name='crateregister'),
    path("result", views.resultsfunction, name="result"),
    path("candidateinformation", views.candidateinformationfunction, name="candidateinformation"),
    path("complaint", views.complaintfunction, name="complaint"),
    path("submitfeedback", views.submitfeedback, name="submitfeedback"),
    path("login", views.login, name="login"),
    path("checkaminlogin", views.checkaminlogin, name="checkaminlogin"),
    path("voting", views.voting, name="voting"),
    path("castvote", views.castvote, name="castvote"),
    path("signup", views.singup, name="signup"),
    path('createuser/', views.createuser, name='createuser'),
    path("logout", views.logout_view, name="logout"),
    path("", include("aminapp.urls")),
]
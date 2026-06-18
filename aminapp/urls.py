from django.urls import path
from . import views

urlpatterns = [
      path("aminhome",views.aminhome,name="aminhome"),
      path("partyvotes", views.partyvotes, name="partyvotes"),
      path("voters", views.voters, name="voters"),    
      
]

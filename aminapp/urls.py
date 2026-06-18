from django.urls import path
from . import views

urlpatterns = [
      path("aminhome",views.aminhome,name="aminhome"),    
]

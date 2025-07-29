from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_zip, name='upload_zip'),
    
]

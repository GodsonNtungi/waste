from django.urls import path
from .views import image_upload,home

urlpatterns = [
    path("",home,name="home"),
    path('image-upload/', image_upload, name='image-upload'),
]

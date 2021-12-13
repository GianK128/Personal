from django.urls import path
from . import views

urlpatterns = [
    path("", views.nothing, name="default"),
    path("hola/", views.hola, name="hola"),
    path("chau/", views.chau, name="chau")
]
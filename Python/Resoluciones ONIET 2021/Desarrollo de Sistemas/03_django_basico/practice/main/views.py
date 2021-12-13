from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def nothing(response):
    return HttpResponse('<a href="/hola">Decir hola</a><br><a href="/chau">Decir chau</a>')

def hola(response):
    return HttpResponse("<h1>¡Hola!</h1>")

def chau(response):
    return HttpResponse("<h1>¡Chau!</h1>")

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'Barber\index.html')

def respond(request):
    return HttpResponse("Made it")

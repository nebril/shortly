from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "shorten/index.html", {})

def item(request):
    return HttpResponse("item view")

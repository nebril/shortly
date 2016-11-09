from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the django app index.")

def item(request):
    return HttpResponse("item view")

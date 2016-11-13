from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from shorten.models import Url


@require_http_methods(["GET"])
def index(request):
    return render(request, "shorten/index.html", {})

@require_http_methods(["GET"])
def item(request):
    return HttpResponse("item view")

@require_http_methods(["POST"])
def shorten(request):
    if request.is_ajax():
       url = request.body

    shortened = Url.new(url)
    return HttpResponse(shortened.shortened_url)

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from shorten.models import Url


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "GET":
        return render(request, "shorten/index.html", {})
    elif request.method == "POST":
        if request.is_ajax():
            url = request.body
            shortened = Url.new(url)
            return HttpResponse(shortened.build_full_url(request))
        else:
            url = request.POST['url']
            shortened = Url.new(url.encode("utf-8"))
            return render(request, "shorten/index.html",
                          {"short": shortened.build_full_url(request),
                           "original": url})

@require_http_methods(["GET"])
def item(request):
    return HttpResponse("item view")

def redirect(request):
    return HttpResponse("redirect")

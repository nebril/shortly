from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django import shortcuts

from shorten.models import Url


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "GET":
        return shortcuts.render(request, "shorten/index.html", {})
    elif request.method == "POST":
        if request.is_ajax():
            url = request.body
            shortened = Url.new(url)
            return HttpResponse(shortened.build_full_url(request))
        else:
            url = request.POST['url']
            shortened = Url.new(url.encode("utf-8"))
            return shortcuts.render(request, "shorten/index.html",
                          {"short": shortened.build_full_url(request),
                           "original": url})

@require_http_methods(["GET"])
def item(request):
    try:
        url = Url.objects.get(shortened_url=request.path[2:])
    except ObjectDoesNotExist:
        raise Http404

    return shortcuts.render(request, "shorten/item.html",
                  {"url": url,
                   "full_shortened": url.build_full_url(request)})

def redirect(request):
    try:
        url = Url.objects.get(shortened_url=request.path[1:])
    except ObjectDoesNotExist:
        raise Http404

    return shortcuts.redirect(url.original_url)

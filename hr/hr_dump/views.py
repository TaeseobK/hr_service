from django.http import HttpResponse
from prometheus_client import generate_latest, REGISTRY

def metrics_view(request):
    return HttpResponse(generate_latest(REGISTRY), content_type="text/plain; charset=utf-8")
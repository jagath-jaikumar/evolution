from django.http import JsonResponse, HttpResponse
from django.db import connections
from datetime import datetime


def root(request):
    return JsonResponse({"message": f"Evolution Server running {datetime.now()}"})


def liveness_check(request):
    return HttpResponse("OK")


def readiness_check(request):
    for connection in connections.all():
        try:
            connection.cursor()
        except Exception as e:
            return HttpResponse(f"Database connection failed: {e}", status=500)
    return HttpResponse("OK")

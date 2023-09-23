from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
# Create your views here.

def handle404(request:HttpRequest, exception):
    return JsonResponse({"error": f"The url {request.path} was not found."}, status=404)


def handle401(request:HttpRequest, exception):
    return JsonResponse({"error": "Unathorized - please log in first."}, status=401)


def handle403(request:HttpRequest, exception):
    return JsonResponse({"error": "You don't have permission to access this resource"}, status=403)


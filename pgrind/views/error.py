from django.http import HttpRequest
from django.shortcuts import render


def error(request: HttpRequest):
    return render(request, "pgrind/error.html")

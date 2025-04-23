from django.http import HttpRequest
from django.shortcuts import render


def error(request: HttpRequest):
    return render(request, "paper_questions/error.html")

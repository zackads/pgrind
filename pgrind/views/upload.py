# uploads/views.py
from django.http import HttpRequest
from django.shortcuts import render, redirect
from pgrind.forms.single_problem_upload_form import SingleProblemUploadForm


def upload(request: HttpRequest):
    if request.method == "POST":
        form = SingleProblemUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pgrind:home")
    else:
        form = SingleProblemUploadForm()
    return render(request, "pgrind/upload.html", {"form": form})

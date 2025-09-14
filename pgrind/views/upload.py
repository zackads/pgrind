from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from pgrind.forms.single_problem_upload_form import SingleProblemUploadForm

from pgrind.models.problem import Problem
from pgrind.models.subject import Subject


def upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SingleProblemUploadForm(request.POST, request.FILES)
        if form.is_valid():
            subject, _ = Subject.objects.get_or_create(
                name=form.cleaned_data["subject"]
            )
            problem = Problem(
                subject=subject,
                question_image=request.FILES["question_image"],
                solution_image=request.FILES["solution_image"],
            )
            problem.save()
            return redirect("pgrind:home")

    form = SingleProblemUploadForm()
    return render(request, "pgrind/upload.html", {"form": form})

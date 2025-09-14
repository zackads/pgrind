from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from pgrind.models.problem import Problem
from pgrind.models.attempt import Attempt

from pgrind.forms.attempt_form import AttemptForm


def solution(request: HttpRequest, id: int):
    problem = get_object_or_404(Problem, id=id)

    if request.method == "POST":
        form = AttemptForm(request.POST or None)

        if form.is_valid():
            attempt = Attempt.objects.create(
                problem=problem,
                confidence=form.cleaned_data["confidence"],
            )
            attempt.save()
            return redirect("pgrind:home")
        else:
            return render(
                request,
                "pgrind/solution.html",
                {
                    "form": form,
                    "problem": problem,
                },
            )
    else:
        return render(
            request,
            "pgrind/solution.html",
            {
                "problem": problem,
            },
        )

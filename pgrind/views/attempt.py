from django.http import HttpRequest
from django.shortcuts import redirect, render

from pgrind.forms.attempt_form import AttemptForm
from pgrind.models.problem import Problem
from pgrind.models.attempt import Attempt


def attempt(request: HttpRequest, id: int):
    if request.method == "POST":
        form = AttemptForm(request.POST or None)
        problem = Problem.objects.get(id=id)

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

from django.shortcuts import get_object_or_404

from django.http import HttpRequest
from django.shortcuts import render

from pgrind.models.problem import Problem
from pgrind.models.attempt import Attempt
from pgrind.models.subject import Subject


def parse_subjects(subjects: str) -> list[str]:
    if subjects == "all":
        return [s.name for s in Subject.objects.distinct()]
    else:
        return subjects.split("-")


def parse_confidences(confidences: str) -> list[str]:
    if confidences == "all":
        return [c[1] for c in Attempt.Confidence.choices]
    else:
        return confidences.split("-")


def question(request: HttpRequest, id: int):
    problem = get_object_or_404(Problem, id=id)
    # attempts = Attempt.objects.get(problem=problem)

    return render(request, "pgrind/question.html", {"problem": problem, "attempts": []})

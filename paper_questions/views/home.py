from django.shortcuts import render
from django.http import HttpRequest

from paper_questions.models import StaticFileProblemAttempt, Subject


def home(request: HttpRequest):
    """Home"""
    subjects = [subject.value for subject in Subject]
    confidences = {
        subject: StaticFileProblemAttempt.get_confidences_by_subject(subject)
        for subject in subjects
    }
    return render(
        request,
        "paper_questions/index.html",
        {
            "confidences": confidences,
        },
    )

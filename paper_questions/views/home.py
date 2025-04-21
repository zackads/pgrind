import os

from django.shortcuts import render

from paper_questions.models import ProblemAttempt

def home(request):
    """Home"""
    subjects = [subject[0] for subject in ProblemAttempt.SUBJECT_CHOICES]
    confidences = {subject: ProblemAttempt.get_confidences_by_subject(subject) for subject in subjects}
    return render(
        request,
        "paper_questions/index.html",
        {
            "confidences": confidences,
        },
    )






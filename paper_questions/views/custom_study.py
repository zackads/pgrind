from django.shortcuts import render

from paper_questions.models import ProblemAttempt


def custom_study(request):
    """Custom study session"""
    subjects = [subject[0] for subject in ProblemAttempt.SUBJECT_CHOICES]

    return render(
        request,
        "paper_questions/custom_study.html",
        {"subjects": [subject[0] for subject in ProblemAttempt.SUBJECT_CHOICES]},
    )

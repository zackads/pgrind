import random

from django.shortcuts import redirect

from pgrind.models import StaticFileProblemAttempt, StaticFileProblem


def random_question(request):
    subject = random.choice(StaticFileProblemAttempt.SUBJECT_CHOICES)[0]
    question = random.randint(1, StaticFileProblem.question_count(subject))
    return redirect("pgrind:question", subject=subject, question=question)

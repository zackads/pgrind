import random

from django.shortcuts import redirect

from paper_questions.models import StaticFileProblemAttempt, StaticFileProblem


def random_question(request):
    subject = random.choice(StaticFileProblemAttempt.SUBJECT_CHOICES)[0]
    question = random.randint(1, StaticFileProblem.question_count(subject))
    return redirect("paper_questions:question", subject=subject, question=question)

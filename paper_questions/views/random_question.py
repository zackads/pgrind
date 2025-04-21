import random

from django.shortcuts import redirect

from paper_questions.models import ProblemAttempt, Problem


def random_question(request):
    subject = random.choice(ProblemAttempt.SUBJECT_CHOICES)[0]
    question = random.randint(1, Problem.question_count(subject))
    return redirect("paper_questions:question", subject=subject, question=question)

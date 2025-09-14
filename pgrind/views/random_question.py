import random

from django.shortcuts import redirect

from pgrind.models import static_file_problem, static_file_problem_attempt


def random_question(request):
    subject = random.choice(static_file_problem_attempt.SUBJECT_CHOICES)[0]
    question = random.randint(1, static_file_problem.question_count(subject))
    return redirect("pgrind:question", subject=subject, question=question)

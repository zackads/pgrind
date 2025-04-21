from django.shortcuts import redirect

from paper_questions.models import ProblemAttempt


def attempt(request, subjects):
    ProblemAttempt.objects.create(
        subject=request.POST.get("subject"),
        question=int(request.POST.get("question")),
        confidence=int(request.POST.get("confidence")),
    )

    return redirect("paper_questions:question.random", subjects=subjects)

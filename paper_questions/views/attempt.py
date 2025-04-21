from django.http import HttpResponseRedirect
from django.urls import reverse

from paper_questions.models import ProblemAttempt


def attempt(request):
    ProblemAttempt.objects.create(
        subject=request.POST.get("subject"),
        question=int(request.POST.get("question")),
        confidence=int(request.POST.get("confidence")),
    )

    return HttpResponseRedirect(reverse("paper_questions:question.random"))

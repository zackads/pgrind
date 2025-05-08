from django.http import HttpRequest
from django.shortcuts import redirect

from paper_questions.models import StaticFileProblemAttempt


def attempt(request: HttpRequest, subjects: str, difficulties: str):
    subject = request.POST.get("subject")
    question = request.POST.get("question")
    confidence = request.POST.get("confidence")

    if not subject or not question or not confidence:
        return redirect("paper_questions:error")

    StaticFileProblemAttempt.objects.create(
        subject=subject,
        question=int(question),
        confidence=int(confidence),
    )

    return redirect(
        "paper_questions:question.random", subjects=subjects, difficulties=difficulties
    )

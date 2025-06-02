from django.http import HttpRequest
from django.shortcuts import redirect

from paper_questions.models import StaticFileProblemAttempt, StaticFileProblem


def attempt(request: HttpRequest, subjects: str, difficulties: str):
    subject = request.POST.get("subject")
    question = request.POST.get("question")
    confidence = request.POST.get("confidence")

    if not subject or not question or not confidence:
        return redirect("paper_questions:error")

    problem = StaticFileProblem.objects.filter(
        subject=subject, question_number=int(question)
    ).first()

    StaticFileProblemAttempt.objects.create(
        problem=problem,
        confidence=int(confidence),
    )

    return redirect(
        "paper_questions:question.random", subjects=subjects, difficulties=difficulties
    )

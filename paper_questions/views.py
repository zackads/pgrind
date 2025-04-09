import os
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import reverse

from paper_questions.models import ProblemAttempt
from pgrind.settings import STATIC_ROOT

files = [f for f in os.listdir(str(STATIC_ROOT) + "/paper_questions")]


def question_count(subject: str) -> int:
    return len([f for f in files if f.split("-")[0] == subject]) // 2


def get_confidences_by_subject(subject: str) -> list[tuple[int, int]]:
    n = question_count(subject)
    confidences = []
    for i in range(1, n + 1):
        attempt = (
            ProblemAttempt.objects.filter(subject=subject, question=i)
            .order_by("attempted_at")
            .first()
        )

        if attempt:
            confidences.append((i, attempt.confidence))
        else:
            confidences.append((i, 0))

    return confidences


def get_attempts(subject: str, question: int) -> list[ProblemAttempt]:
    return list(
        ProblemAttempt.objects.filter(subject=subject, question=question).order_by(
            "attempted_at"
        )
    )


def home(request):
    """Home"""
    subjects = [subject[0] for subject in ProblemAttempt.SUBJECT_CHOICES]
    confidences = {subject: get_confidences_by_subject(subject) for subject in subjects}
    return render(
        request,
        "paper_questions/index.html",
        {
            "confidences": confidences,
        },
    )


def question(request, subject, question):
    def days_ago_text(n: int) -> str:
        if n == 0:
            return "today"
        elif n == 1:
            return "yesterday"
        else:
            return str(n) + " days ago"

    return render(
        request,
        "paper_questions/question.html",
        {
            "subject": subject,
            "question": question,
            "attempts": [
                {"days_ago": days_ago_text(a.days_ago()), "confidence": a.confidence}
                for a in get_attempts(subject, question)
            ],
            "image_url": static(f"paper_questions/{subject}-q-{question}.png"),
            "solution_url": f"/solution?subject={subject}&question={question}",
        },
    )


def random_question(request):
    subject = random.choice(ProblemAttempt.SUBJECT_CHOICES)[0]
    question = random.randint(1, question_count(subject))
    return redirect("paper_questions:question", subject=subject, question=question)


def attempt(request):
    ProblemAttempt.objects.create(
        subject=request.POST.get("subject"),
        question=int(request.POST.get("question")),
        confidence=int(request.POST.get("confidence")),
    )

    return HttpResponseRedirect(reverse("paper_questions:random_question"))


def solution(request, subject, question):
    return render(
        request,
        "paper_questions/solution.html",
        {
            "subject": subject,
            "question": question,
            "image_url": static(f"paper_questions/{subject}-s-{question}.png"),
        },
    )

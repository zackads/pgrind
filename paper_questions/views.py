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


def home(request):
    """Home"""
    return render(request, "paper_questions/index.html")


def question(request):
    subjects = ["data", "prob_ii", "comp_arch"]
    subject = request.GET.get("subject")
    question = request.GET.get("question")
    if not subject or not id:
        subject = random.choice(subjects)
        question = random.randint(1, question_count(subject))
        return redirect(f"{request.path}?subject={subject}&question={question}")

    return render(
        request,
        "paper_questions/question.html",
        {
            "subject": subject,
            "question": question,
            "image_url": static(f"paper_questions/{subject}-q-{question}.png"),
            "solution_url": f"/solution?subject={subject}&question={question}",
        },
    )


def attempt(request):
    ProblemAttempt.objects.create(
        subject=request.POST.get("subject"),
        question=int(request.POST.get("question")[0]),
        confidence=int(request.POST.get("confidence")[0]),
    )

    return HttpResponseRedirect(reverse("paper_questions:question"))


def solution(request):
    subject = request.GET.get("subject")
    question = request.GET.get("question")

    return render(
        request,
        "paper_questions/solution.html",
        {
            "subject": subject,
            "question": question,
            "image_url": static(f"paper_questions/{subject}-s-{question}.png"),
            "question_url": f"/question?subject={subject}&question={question}",
        },
    )

import random

from typing import Optional

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.templatetags.static import static

from pgrind.models import StaticFileProblemAttempt, StaticFileProblem


def days_ago_text(n: int) -> str:
    if n == 0:
        return "today"
    elif n == 1:
        return "yesterday"
    else:
        return str(n) + " days ago"


def parse_subjects(subjects: str) -> list[str]:
    if subjects == "all":
        return [s.value for s in StaticFileProblem.Subject]
    else:
        return subjects.split("-")


def parse_difficulties(difficulties: str) -> list[str]:
    if difficulties == "all":
        return [c[1] for c in StaticFileProblemAttempt.Confidence.choices]
    else:
        return difficulties.split("-")


def question(
    request: HttpRequest,
    subjects: str = "all",
    difficulties: str = "all",
    subject: Optional[str] = None,
    question: Optional[int] = None,
):
    attempts = [
        {
            "days_ago": days_ago_text(attempt.days_ago()),
            "confidence": attempt.confidence,
        }
        for attempt in StaticFileProblemAttempt.objects.filter(
            problem__subject=subject, problem__question_number=question
        )
    ]

    if subject:
        if question:
            return render(
                request,
                "pgrind/question.html",
                {
                    "subjects": subjects,
                    "difficulties": difficulties,
                    "subject": subject,
                    "question": question,
                    "attempts": attempts,
                    "image_url": static(f"pgrind/{subject}-q-{question}.png"),
                    "solution_url": f"/solution?subject={subject}&question={question}",
                },
            )
        else:
            random_question = random.randint(
                1, StaticFileProblem.objects.filter(subject=subject).count()
            )
            return redirect(
                "pgrind:question",
                subjects=subjects,
                difficulties=difficulties,
                subject=subject,
                question=random_question,
            )
    else:
        random_subject = random.choice(parse_subjects(subjects))
        random_question = random.randint(
            1, StaticFileProblem.objects.filter(subject=random_subject).count()
        )

        return redirect(
            "pgrind:question",
            subjects=subjects,
            difficulties=difficulties,
            subject=random_subject,
            question=random_question,
        )


def get_attempts(subject: str, question: int) -> list[StaticFileProblemAttempt]:
    if question < StaticFileProblem.objects.filter(subject=subject).count():
        return list(
            StaticFileProblemAttempt.objects.filter(
                subject=subject, question=question
            ).order_by("attempted_at")
        )
    else:
        return []

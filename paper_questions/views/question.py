import random

from django.shortcuts import render, redirect
from django.templatetags.static import static

from paper_questions.models import ProblemAttempt, Problem


def days_ago_text(n: int) -> str:
    if n == 0:
        return "today"
    elif n == 1:
        return "yesterday"
    else:
        return str(n) + " days ago"


def question(
    request,
    subject=None,
    question=None,
):
    if subject:
        if question:
            return render(
                request,
                "paper_questions/question.html",
                {
                    "subject": subject,
                    "question": question,
                    "attempts": [
                        {
                            "days_ago": days_ago_text(a.days_ago()),
                            "confidence": a.confidence,
                        }
                        for a in get_attempts(subject, question)
                    ],
                    "image_url": static(f"paper_questions/{subject}-q-{question}.png"),
                    "solution_url": f"/solution?subject={subject}&question={question}",
                },
            )
        else:
            random_question = random.randint(1, Problem.question_count(subject))
            return redirect(
                "paper_questions:question", subject=subject, question=random_question
            )
    else:
        random_subject = random.choice(ProblemAttempt.SUBJECT_CHOICES)[0]
        random_question = random.randint(1, Problem.question_count(random_subject))

        return redirect(
            "paper_questions:question", subject=random_subject, question=random_question
        )


def get_attempts(subject: str, question: int) -> list[ProblemAttempt]:
    if question < Problem.question_count(subject):
        return list(
            ProblemAttempt.objects.filter(subject=subject, question=question).order_by(
                "attempted_at"
            )
        )
    else:
        return []

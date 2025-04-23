from datetime import datetime, timezone
from enum import Enum

from django.db import models

from .Problem import Problem
from .Subject import Subject


class ProblemAttempt(models.Model):
    """
    Record the outcome of an attempt to answer a problem posed by the app, and thus determine when the question is next
    posed to the user.
    """

    class Difficulty(Enum):
        NOT_ATTEMPTED = "not_attempted"
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    CONFIDENCE_CHOICES = [
        (0, "not_attempted"),
        (1, "hard"),
        (2, "medium"),
        (3, "easy"),
    ]

    subject = models.CharField(
        max_length=20, choices=[(s.value, s.value) for s in Subject]
    )
    question = models.CharField(max_length=20)
    attempted_at = models.DateTimeField(auto_now_add=True)
    confidence = models.IntegerField(choices=CONFIDENCE_CHOICES)

    def __str__(self):
        return f"{self.subject} - {self.question} at {self.attempted_at}, confidence {self.confidence}"

    def days_ago(self, now: datetime = datetime.now(timezone.utc)) -> int:
        return (now - self.attempted_at).days

    @staticmethod
    def get_confidences_by_subject(subject: str) -> list[tuple[int, int]]:
        n = Problem.question_count(subject)

        confidences: list[tuple[int, int]] = []
        for i in range(1, n + 1):
            attempt = (
                ProblemAttempt.objects.filter(subject=subject, question=i)
                .order_by("attempted_at")
                .last()
            )

            if attempt:
                confidences.append((i, attempt.confidence))
            else:
                confidences.append((i, 0))

        return confidences

from datetime import datetime, timezone

from django.db import models

from .Problem import Problem


class ProblemAttempt(models.Model):
    """
    Record the outcome of an attempt to answer a problem posed by the app, and thus determine when the question is next
    posed to the user.
    """

    SUBJECT_CHOICES = [
        ("comp_arch", "Computer Architecture"),
        ("prob_ii", "Probability II"),
        ("data", "Data"),
    ]
    CONFIDENCE_CHOICES = [
        (1, "Hard"),
        (2, "Medium"),
        (3, "Easy"),
    ]

    attempted_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    question = models.CharField(max_length=20)
    confidence = models.IntegerField(choices=CONFIDENCE_CHOICES)

    def __str__(self):
        return f"{self.subject} - {self.question} at {self.attempted_at}, confidence {self.confidence}"

    def days_ago(self, now=datetime.now(timezone.utc)) -> int:
        return (now - self.attempted_at).days

    @staticmethod
    def get_confidences_by_subject(subject: str) -> list[tuple[int, int]]:
        n = Problem.question_count(subject)

        confidences = []
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

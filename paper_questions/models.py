# Create your models here.

from django.db import models


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
        (0, "Hard"),
        (1, "Medium"),
        (2, "Easy"),
    ]

    attempted_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    question = models.CharField(max_length=20)
    confidence = models.IntegerField(choices=CONFIDENCE_CHOICES)

    def __str__(self):
        return f"{self.subject} - {self.question} at {self.attempted_at}, confidence {self.confidence}"

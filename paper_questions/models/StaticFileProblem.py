from django.db import models
from django.core.validators import MinValueValidator


class StaticFileProblem(models.Model):
    class Subject(models.TextChoices):
        COMP_ARCH = "comp_arch", "computer architecture"
        DATA = "data", "data-driven computer science"
        PROB_2 = "prob_ii", "probability 2"

    @staticmethod
    def get_subject_keys():
        return [choice[0] for choice in StaticFileProblem.Subject.choices]

    subject = models.CharField(
        max_length=9,
        choices=Subject,
    )
    question_number = models.IntegerField(validators=[MinValueValidator(1)])
    static_problem_path = models.CharField(max_length=255)
    static_solution_path = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "question_number"], name="unique_problem"
            )
        ]

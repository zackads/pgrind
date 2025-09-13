import os

from django.test import TestCase
from django.conf import settings


class QuestionTestCase(TestCase):
    def test_number_of_solutions_equals_number_of_questions(self):
        static_dir = os.path.join(settings.STATIC_ROOT, "pgrind")
        files = [f for f in os.listdir(static_dir)]

        for _, f in enumerate(files, start=1):
            subject, q_or_s, n = f.split(".")[0].split("-")
            n = int(n)

            # every question has a solution; every solution has a question
            if q_or_s == "q":
                self.assertTrue(
                    f"{subject}-s-{n}.png" in files, f"{subject}-s-{n}.png not found"
                )
            if q_or_s == "s":
                self.assertTrue(
                    f"{subject}-q-{n}.png" in files, f"{subject}-q-{n}.png not found"
                )

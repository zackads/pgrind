from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from django.core.management.base import CommandError
import os
import re

from pgrind.models import StaticFileProblem
from django.conf import settings
from pathlib import Path


class Command(CollectStaticCommand):
    help = "Collect static files and update the database with their paths."

    def handle(self, *args, **options):
        super().handle(*args, **options)

        self.stdout.write("Now adding StaticFileProblems to the database...")

        try:
            load_static_metadata()
        except Exception as e:
            raise CommandError(
                f"Error while adding StaticFileProblems to the database: {e}"
            )
        self.stdout.write(
            self.style.SUCCESS("Successfully added StaticFileProblems to the database.")
        )


def load_static_metadata():
    STATIC_DIR = os.path.join(settings.STATIC_ROOT, "pgrind")

    pattern = re.compile(r"(?P<subject>[\w-]+)-q-(?P<number>\d+)\.png")

    for filename in os.listdir(STATIC_DIR):
        match = pattern.match(filename)
        if match:
            subject = match.group("subject")
            number = int(match.group("number"))

            path = Path(STATIC_DIR + "/" + filename).name
            StaticFileProblem.objects.get_or_create(
                subject=subject,
                question_number=number,
                static_problem_path=path,
                static_solution_path=path.replace("-q-", "-s-"),
            )

import os

from pgrind.settings import STATIC_ROOT

files = [f for f in os.listdir(str(STATIC_ROOT) + "/paper_questions")]


class Problem:
    """
    Not a Django model because questions are persisted to filesystem.
    """

    SUBJECTS = ["comp_arch", "prob_ii", "data"]

    @staticmethod
    def question_count(subject: str) -> int:
        return len([f for f in files if f.split("-")[0] == subject]) // 2

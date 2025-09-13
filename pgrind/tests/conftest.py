import sys


from pytest import TestReport


def pytest_runtest_logreport(report: TestReport):
    if report.when == "call" and report.failed:
        # Plays a beep sound using the terminal bell character
        sys.stdout.write("\a")
        sys.stdout.flush()

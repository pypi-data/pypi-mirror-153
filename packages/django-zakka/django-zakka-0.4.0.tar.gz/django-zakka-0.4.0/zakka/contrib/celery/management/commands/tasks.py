from pprint import pprint

from celery import current_app

from django.core.management.base import BaseCommand
from django.test import override_settings

from zakka.mixins.command import LoggingMixin


class Command(LoggingMixin, BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("--eager", action="store_true")
        parser.add_argument("task", nargs="?")
        parser.add_argument("rest", nargs="*")

    def handle(self, task, eager, rest, **options):
        current_app.loader.import_default_modules()
        if task in current_app.tasks:
            with override_settings(CELERY_TASK_ALWAYS_EAGER=eager):
                result = current_app.tasks[task](*rest)
                if hasattr(result, "__iter__"):
                    result = list(result)
                pprint(result)
        else:
            for task in sorted(current_app.tasks):
                print(task)

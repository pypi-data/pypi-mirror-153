from celery import current_app
from celery.app.task import Task
from celery.schedules import maybe_schedule


class PeriodicTask(Task):
    relative = False
    options = None

    def __init__(self):
        if not hasattr(self, "run_every"):
            raise NotImplementedError("Periodic tasks must have a run_every attribute")
        self.run_every = maybe_schedule(self.run_every, self.relative)
        super().__init__()

    @classmethod
    def on_bound(cls, app):
        app.conf.beat_schedule[cls.name] = {
            "task": cls.name,
            "schedule": cls.run_every,
            "args": (),
            "kwargs": {},
            "options": cls.options or {},
            "relative": cls.relative,
        }


def periodic_task(*args, **kwargs):
    return current_app.task(*args, **dict({"base": PeriodicTask}, **kwargs))

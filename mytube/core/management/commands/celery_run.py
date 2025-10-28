import subprocess, sys
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Run Celery worker (and optionally Beat) in background"

    def add_arguments(self, parser):
        parser.add_argument(
            "--beat", action="store_true",
            help="Also start Celery Beat scheduler",
        )
        parser.add_argument(
            "--loglevel", default="info",
            help="Logging level (default: info)",
        )
        parser.add_argument(
            "--pool", default="prefork",
            help="How to complete tasks",
        )

    def handle(self, *args, **options):
        project_name = "mytube"
        python_path = sys.executable
        base_dir = settings.BASE_DIR

        self.stdout.write("Starting Celery worker...")
        subprocess.Popen(
            [python_path, "-m", "celery", "-A", project_name, "worker", "-l", options["loglevel"], "--pool", options["pool"]],
            cwd=base_dir,
        )

        if options["beat"]:
            self.stdout.write("Starting Celery Beat scheduler...")
            subprocess.Popen(
                [python_path, "-m", "celery", "-A", project_name, "beat", "-l", options["loglevel"]],
                cwd=base_dir,
            )

            self.stdout.write(self.style.SUCCESS("Celery started in background"))
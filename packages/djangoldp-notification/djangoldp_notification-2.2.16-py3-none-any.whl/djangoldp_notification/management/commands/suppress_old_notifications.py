from textwrap import dedent
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from djangoldp_notification.models import Notification


def _compute_time_limit(timeout):
    """
    >>> _compute_time_limit('10')
    10
    >>> _compute_time_limit('10h')
    600
    >>> _compute_time_limit('10m')
    10
    >>> _compute_time_limit('10d')
    14400
    """
    try:
        if timeout.endswith("d"):
            return int(timeout[:-1]) * 24 * 60
        elif timeout.endswith("h"):
            return int(timeout[:-1]) * 60
        elif timeout.endswith("m"):
            return int(timeout[:-1])
        else:
            return int(timeout)
    except ValueError:
        raise CommandError("--older option is not correct")


class Command(BaseCommand):
    help = "Suppress notifications older than 72h"

    def add_arguments(self, parser):
        parser.add_argument(
            "--older",
            action="store",
            default="72h",
            help=dedent(
                """
                Set a different time period for notifications to be deleted. Default is 72h
                This parameters takes a interger value in minutes by default. 'd', 'h' and 'm' suffix also work.
                Examples: --older 10d, --older 10
                """
            ),
        )

    def handle(self, *args, **options):
        older_than = _compute_time_limit(options["older"])
        limit = datetime.today() - timedelta(minutes=older_than)
        Notification.objects.filter(date__lte=limit).delete()

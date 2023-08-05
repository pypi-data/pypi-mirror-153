from django.core.management.base import BaseCommand, CommandError
from djangoldp_notification.factories import NotificationFactory

class Command(BaseCommand):
    help = 'Mock data'

    def add_arguments(self, parser):
        parser.add_argument('--size', type=int, default=0, help='Number of notifications to create')

    def handle(self, *args, **options):
        NotificationFactory.create_batch(options['size'])
        self.stdout.write(self.style.SUCCESS('Successful data mock install'))

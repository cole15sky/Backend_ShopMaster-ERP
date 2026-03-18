from django.core.management.base import BaseCommand
from utils.seeds import seed_users  # optional if needed
import utils.seeds  # this will run the file


class Command(BaseCommand):
    help = "Seed users"

    def handle(self, *args, **kwargs):
        import utils.seeds
        self.stdout.write(self.style.SUCCESS("Seeding completed"))
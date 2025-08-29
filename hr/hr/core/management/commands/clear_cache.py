from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "Clear user cache (user:* keys)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--id",
            type=str,
            help="Comma-separated user IDs to clear cache for, e.g. --id=1,7,9",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Clear ALL cache (warning: this will remove everything, not only user:*)",
        )

    def handle(self, *args, **options):
        ids = options.get("id")
        clear_all = options.get("all")

        if clear_all:
            cache.clear()
            self.stdout.write(self.style.SUCCESS("Cleared ALL cache."))
            return

        if ids:
            ids = [i.strip() for i in ids.split(",")]
            for uid in ids:
                cache.delete(f"user:{uid}")
            self.stdout.write(self.style.SUCCESS(f"Cleared cache for user IDs: {','.join(ids)}"))
        else:
            self.stdout.write(self.style.WARNING("No --id or --all provided. Nothing cleared."))
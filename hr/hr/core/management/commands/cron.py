import datetime
from django.core.management.base import BaseCommand
from .dump_data import Command as HRDump
from .server_check import Command as ServerCheck


class Command(BaseCommand):
    help = "Cron scheduler to running all the task."

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        day, hour, minute = now.day, now.hour, now.minute

        self.stdout.write(f"[scheduler] Running {now.isoformat()}")

        if day == 1 and hour == 0 and minute <= 30:
            self.stdout.write("[scheduler] Running dump data()...")
            HRDump.run_dump()
        
        if hour == 3 and minute <= 30:
            self.stdout.write("[scheduler] Checking server resource and performance...")
            ServerCheck.run_check(self)

        else:
            self.stdout.write(f"[scheduler] Pass now day: {day}, hour: {hour}, minute: {minute}")
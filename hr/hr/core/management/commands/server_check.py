import json
import datetime
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from hr_dump.models import HRDump

import requests
import psutil

from hr.local_settings import CHAT_IDS, TELEGRAM_TOKEN

class Command(BaseCommand):
    help = "Run checking server data."

    def handle(self, *args, **options):
        self.run_check()

    def run_check(self):
        now = datetime.datetime.now()
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()

        msg = (
            f"📊 HR Server Monitoring\n"
            f"⏰ {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"💻 CPU Usage: {cpu_percent}%\n"
            f"🧠 Memory Usage: {mem.percent}% ({mem.used / (1024**3):.2f} GB used)\n"
            f"💾 Disk Usage: {disk.percent}% ({disk.used / (1024**3):.2f} GB used)\n"
            f"📡 Network: Sent {net.bytes_sent / (1024**2):.2f} MB, Recv {net.bytes_recv / (1024**2):.2f} MB"
        )

        for i in CHAT_IDS:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": i,
                "text": msg,
                "parse_mode": "HTML"
            }
            try:
                resp = requests.post(url, data=payload)
                if resp.status_code == 200:
                    self.stdout.write("[Telegram] Message sent successfully")
                else:
                    self.stdout.write(f"[Telegram] Failed: {resp.text}")
            except Exception as e:
                self.stdout.write(f"[Telegram] Exception: {e}")
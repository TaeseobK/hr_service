import json
import datetime
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from hr_dump.models import HRDump

from hr.local_settings import TELEGRAM_TOKEN, CHAT_IDS

import requests

class Command(BaseCommand):
    help = "Dump data HR_DUMP to JSON (monthly), then delete all data from database."

    def handle(self, *args, **options):
        self.run_dump()

    @staticmethod
    def run_dump():
        """Ambil semua HR_DUMP bulan ini → simpan JSON → hapus DB"""
        now = datetime.datetime.now()
        month_str = now.strftime("%m")
        year_str = now.strftime("%Y")

        # ambil data dari DB alias hr_dump
        qs = HRDump.objects.using("hr_dump").filter(
            created_at__year=year_str,
            created_at__month=month_str,
        )

        if not qs.exists():
            print(f"[HR_DUMP] There's no record for {month_str}/{year_str}")
            return None

        # bentuk list data
        data = [
            {
                "id": obj.id,
                "user_id": obj.user_id,
                "path": obj.path,
                "method": obj.method,
                "payload": obj.payload,
                "created_at": obj.created_at.isoformat(),
            }
            for obj in qs
        ]

        # simpan file ke folder dumps/
        dumps_dir = Path(settings.BASE_DIR) / "dumps"
        dumps_dir.mkdir(parents=True, exist_ok=True)
        filename = f"hr_{month_str}.json"
        filepath = dumps_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[HR_DUMP] Data saved successfully at {filepath}")

        for i in CHAT_IDS:
            send_json(
                file_path=filepath,
                token=TELEGRAM_TOKEN,
                chat_id=i,
                row_count=len(data),
                month_str=month_str,
                year_str=year_str
            )

        # hapus data setelah dump
        count, _ = qs.delete()
        print(f"[HR_DUMP] {count} records deleted after dump")

        return filepath
    
def send_json(file_path, token, chat_id, row_count=0, month_str="", year_str=""):
    url = f"https://api.telegram.org/bot{token}/sendDocument"

    if not Path(file_path).exists():
        print(f"[ERROR] Can't find {file_path}!")
        return None

    caption = (
        f"📦 *HR Dump Report*\n\n"
        f"🗓 Month: *{month_str}/{year_str}*\n"
        f"📊 Total Rows: *{row_count}*\n"
        f"📁 File: `{Path(file_path).name}`\n\n"
        f"✅ Data saved successfully and already sended!"
    )

    with open(file_path, "rb") as f:
        res = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "caption": caption,
                "parse_mode": "Markdown",
            },
            files={"document": f},
        )
        
    return res
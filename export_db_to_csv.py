import csv
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
EXPORT_DATE = datetime.today().strftime('%d%m%Y')

connection = sqlite3.connect(ROOT / "articles.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Article")

with (ROOT / f"export_all_{EXPORT_DATE}.csv").open("w", encoding="utf-8", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(column[0] for column in cursor.description)
    writer.writerows(cursor)

connection.close()
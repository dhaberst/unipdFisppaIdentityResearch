import csv
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DATABASE_PATH = ROOT / "articles.db"

SCRIPTS = ["sample_all_classifications_equal_1"]
EXPORT_DATE = datetime.today().strftime('%d%m%Y')

def sample_all_classifications_equal_1():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT *
            FROM Article
            WHERE gemmaClassification = 1
              AND llamaClassification = 1
              AND phiClassification = 1
            ORDER BY RANDOM()
            LIMIT 20
            """
        )

        with (ROOT / f"export_all_equal_1_{EXPORT_DATE}.csv").open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column[0] for column in cursor.description)
            writer.writerows(cursor)

    print(f"Export saved")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in SCRIPTS:
        available_scripts = ", ".join(SCRIPTS)
        raise SystemExit(
            f"Usage: python3 scripts.py <script>\nAvailable scripts: {available_scripts}"
        )

    if sys.argv[1] == "sample_all_classifications_equal_1":
        sample_all_classifications_equal_1()
        
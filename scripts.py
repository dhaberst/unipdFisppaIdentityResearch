import csv
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DATABASE_PATH = ROOT / "articles.db"

SCRIPTS = ["sample_all_classifications_equal_1", "sample_all_classifications_equal_1_or_2", "sample_classifications_two_equal_1"]
EXPORT_DATE = datetime.today().strftime('%d%m%Y')
EXCLUDE_LIST = ["10acaed5-5d42-47c9-b8ea-c5dd3436001a", "5be0a49a-35a3-4545-ba5f-1e5dadebb70c", "92fa0776-5ece-477d-9d03-244ee0bc6198", "a49bdeb8-6c53-49fa-9a19-0b888de44aaf", "05118859-6e7b-425a-8675-997203535b7f", "131072a8-0bf0-430a-b996-eb79baf0a374", "0b0bc477-8b6e-41a2-bee9-1e44ea5c3446", "d3e9101c-29fc-4f03-b8e5-fc2a4004bf25", "609574e8-cc5f-4d3e-b16c-472f63196692", "b8e2f544-0398-479a-92e1-bb1421e92169", "71df4510-9ef0-45d0-b433-a21f40754056", "57867d67-2db0-4bae-8e6f-d3ba2ffe22ad", "8e2b5225-0d1a-438e-81bb-c55abc0c61f9", "f86ac3c1-37ba-45a8-baae-9c742b134a4e", "01fd48f9-4943-4b64-a007-44febadb1849", "dd1cceb7-1cf5-43c1-97a4-07b6bc7c43b0", "8329e8ec-2005-428b-8d22-b45e394edf36", "e4558dbc-c8cb-41da-8cde-2333df938ec2", "692d6769-c921-406c-add6-55bc2d42ff77", "b0673999-8f10-44f6-b49c-0228c3ec715f", "458b16b0-9145-49b5-aeb8-93c82e8b89d5", "10c3dd8e-8762-4c69-885f-16e38faab390", "6ee0e467-bf14-4d1c-8887-0ae031600da3", "2759f88a-9d73-4aa0-916b-faee458715dd", "b599ffb4-177b-4edc-95de-b9f5776fc92e", "bf1f7246-6822-44cd-bb81-1cf2dc82aa8d", "edfb8eaf-360a-4e24-a0de-6fdf3c10dd12", "4f05616c-2224-4d10-8436-e33986406c5a", "f1b80cba-ae5c-4ff2-8942-94fa2976a370", "d4fc6a12-9987-4090-837c-e8122f97147e"]

def sample_classifications_two_equal_1():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT *
            FROM Article
            WHERE gemmaClassification IS NOT NULL
            AND llamaClassification IS NOT NULL
            AND phiClassification IS NOT NULL
            AND gemmaClassification IN (0, 1)
            AND llamaClassification IN (0, 1)
            AND phiClassification IN (0, 1)
            AND gemmaClassification + llamaClassification + phiClassification = 2
            AND version = 1
            ORDER BY RANDOM()
            """
        )

        with (ROOT / f"export_classifications_two_equal_1_{EXPORT_DATE}.csv").open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column[0] for column in cursor.description)
            writer.writerows(cursor)

    print(f"Export saved")

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
            LIMIT 30
            """
        )

        with (ROOT / f"export_all_equal_1_{EXPORT_DATE}.csv").open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column[0] for column in cursor.description)
            writer.writerows(cursor)

    print(f"Export saved")

def sample_all_classifications_equal_1_or_2():
    with sqlite3.connect(DATABASE_PATH) as connection:
        placeholders = ", ".join("?" for _ in EXCLUDE_LIST)
        exclude_clause = (
            f"AND identifier NOT IN ({placeholders})"
            if EXCLUDE_LIST
            else ""
        )
        cursor = connection.execute(
            f"""
            SELECT identifier, title, fullText, source
            FROM Article
            WHERE gemmaClassification IN (1, 2)
                AND llamaClassification IN (1, 2)
                AND phiClassification IN (1, 2)
                {exclude_clause}
                AND version = 1
            ORDER BY RANDOM()
            """,
            tuple(EXCLUDE_LIST),
        )

        with (ROOT / f"export_all_equal_1_or_2_{EXPORT_DATE}.csv").open("w", encoding="utf-8", newline="") as csv_file:
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
    elif sys.argv[1] == "sample_all_classifications_equal_1_or_2":
        sample_all_classifications_equal_1_or_2()
    elif sys.argv[1] == "sample_classifications_two_equal_1":
        sample_classifications_two_equal_1()
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path
from queries import *

ROOT = Path(__file__).resolve().parent
DATABASE_PATH = ROOT / "articles.db"

def main():
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()

        table_exists = cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'Article'"
        ).fetchone()

        if table_exists is None:
            raise sqlite3.OperationalError("Article table does not exist")

        queries = {
            "All = 1": QUERY_ALL_AGREEMENT_SQL,
            "All = 1 or 2": QUERY_ALL_OR_AMBIGUOUS_SQL,
            "At most 2 = 1": QUERY_AT_MOST_TWO_AGREEMENT_SQL,
            "At most 2 = 1 or 2": QUERY_AT_MOST_TWO_OR_AMBIGUOUS_SQL,
            "At most 1 = 1": QUERY_AT_MOST_ONE_AGREEMENT_SQL,
            "At most 1 = 1 or 2": QUERY_AT_MOST_ONE_OR_AMBIGUOUS_SQL,
            "All = 0": QUERY_ALL_ZERO_SQL,
        }
        counts = [
            cur.execute(f"SELECT COUNT(*) FROM ({query})").fetchone()[0]
            for query in queries.values()
        ]

    fig, ax = plt.subplots()
    ax.bar(queries.keys(), counts)
    ax.set_ylabel("Article count")
    ax.set_title("Article counts by classification")
    ax.tick_params(axis="x", labelrotation=30)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

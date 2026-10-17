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

        plot_model_classification_counts(cur)
        plot_model_classification_performance(cur)

def plot_model_classification_counts(cur):
    queries = {
        "All = 1": QUERY_ALL_AGREEMENT_SQL,
        "All = 1 or 2": QUERY_ALL_OR_AMBIGUOUS_SQL,
        "At most two = 1": QUERY_AT_MOST_TWO_AGREEMENT_SQL,
        "At most two = 1 or 2": QUERY_AT_MOST_TWO_OR_AMBIGUOUS_SQL,
        "At most one = 1": QUERY_AT_MOST_ONE_AGREEMENT_SQL,
        "At most one = 1 or 2": QUERY_AT_MOST_ONE_OR_AMBIGUOUS_SQL,
        "All = 0": QUERY_ALL_ZERO_SQL,
    }

    counts = [
        cur.execute(f"SELECT COUNT(*) FROM ({query})").fetchone()[0]
        for query in queries.values()
    ]

    fig, ax = plt.subplots()
    ax.bar(queries.keys(), counts)
    ax.set_ylabel("Article count")
    ax.set_title("Article counts by classification (Version 1)")
    ax.tick_params(axis="x", labelrotation=30)
    fig.tight_layout()
    plt.show()

def plot_model_classification_performance(cur):
    models = {
        "Gemma": "gemmaClassification",
        "Llama": "llamaClassification",
        "Phi": "phiClassification",
    }
    categories = ["= 1", "= 1 or 2", "= 0"]
    counts_by_model = {
        model: cur.execute(
            QUERY_MODEL_CLASSIFICATION_COUNTS_SQL.format(
                classification_column=column
            )
        ).fetchone()
        for model, column in models.items()
    }

    model_names = list(models)
    for category_index, category in enumerate(categories):
        fig, ax = plt.subplots()
        ax.bar(
            model_names,
            [counts_by_model[model][category_index] for model in model_names],
        )
        ax.set_ylabel("Article count")
        ax.set_title(f"Model counts for classification {category} (Version 1)")
        fig.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()

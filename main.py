import csv
import sqlite3
from pathlib import Path

import ollama

ROOT = Path(__file__).resolve().parent
ARTICLES_FOLDER = ROOT / "articles"
DATABASE_PATH = ROOT / "articles.db"
MODELS = {
    "gemma": "gemma4:12b",
    "llama": "llama3.1:8b",
    "phi": "phi4",
}

PROMPT_VERSION_1 = """
    Role:
    You are an expert in classifying news articles. Your task is to determine whether an article discusses human identity and, specifically, whether that identity is linked to a part of the body (e.g. brain, DNA, genes, blood, heart, the body as a whole or, at most, digital identity). Use one of the following labels: 1 for Relevant, 0 for Not Relevant or 2 Ambiguous. Ambiguous should not be a catch-all, only when the article discusses human identity, but the reference to a part of the body is only partial or not clearly defined.

    Label descriptions:
    Relevant: the article discusses human identity and makes a clear reference to a part of the body in describing that identity.
    Not Relevant: the article does not discuss human identity.
    Ambiguous: the article discusses human identity, but the reference to a part of the body is only partial or not clearly defined.

    Response Requirement:
    Output only a single integer: 1 for Relevant, 0 for Not Relevant, 2 Ambiguous. Do not include any other numbers, symbols, or characters.

    Article to classify:
    Title: {title}

    Text:
    {article_text}
"""

def main():
    with sqlite3.connect(DATABASE_PATH) as con:
        populate_database(con.cursor())

        run_gemma_classification(con)

def populate_database(cur):
    table_exists = cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'Article'"
    ).fetchone()

    if table_exists:
        return

    print(f"Populating database from {ARTICLES_FOLDER}")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Article (
            Id INTEGER PRIMARY KEY,
            identifier TEXT NOT NULL UNIQUE,
            title TEXT,
            url TEXT,
            date TEXT,
            fullText TEXT,
            source TEXT,
            bodyPart TEXT,
            gemmaClassification INTEGER CHECK (gemmaClassification IN (0, 1, 2)),
            llamaClassification INTEGER CHECK (llamaClassification IN (0, 1, 2)),
            phiClassification INTEGER CHECK (phiClassification IN (0, 1, 2)),
            version INTEGER NOT NULL DEFAULT 1
        );
    """)

    required_columns = {"Fulltext", "Identifier", "Date", "Source Set", "Title", "URL"}
    insert_article = """
        INSERT INTO Article (
            identifier, title, url, date, fullText, source, bodyPart, version
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """

    csv_files = sorted(ARTICLES_FOLDER.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {ARTICLES_FOLDER}")
        return

    for path in csv_files:
        imported = 0
        skipped = 0

        print(f"Reading {path.name}")
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            missing_columns = required_columns - set(reader.fieldnames or ())

            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(f"{path} is missing required CSV columns: {missing}")

            for row in reader:
                identifier = row["Identifier"]
                if not identifier:
                    raise ValueError(f"{path} contains a row without an Identifier")

                exists = cur.execute(
                    "SELECT 1 FROM Article WHERE identifier = ?",
                    (identifier,),
                ).fetchone()

                if exists:
                    skipped += 1
                    print(
                        f"Skipped {identifier} from {path.name}: "
                        "identifier already exists in Article"
                    )
                    continue

                cur.execute(
                    insert_article,
                    (
                        identifier,
                        row["Title"],
                        row["URL"],
                        row["Date"],
                        row["Fulltext"],
                        row["Source Set"],
                        path.stem,
                    ),
                )

                imported += 1

        print(f"Finished {path.name}: imported {imported}, skipped {skipped} existing")

def run_gemma_classification(con):
    articles = con.execute(
        """
        SELECT Id, identifier, title, fullText
        FROM Article
        WHERE gemmaClassification IS NULL
        ORDER BY Id
        """
    ).fetchall()

    if not articles:
        print("No articles need Gemma classification")
        return

    print(f"Starting Gemma classification for {len(articles)} articles")

    for number, (article_id, identifier, title, full_text) in enumerate(articles, start=1):
        print(f"Classifying article {number}/{len(articles)}: {title or identifier}")

        if title == "" or full_text == "":
            print(f"Title or Text is missing skipping identifier {identifier}")

        prompt = PROMPT_VERSION_1.format(title=title, article_text=full_text)

        response = ollama.chat(
            model=MODELS["gemma"],
            messages=[{"role": "user", "content": prompt}],
            options={"num_ctx": 16384, "temperature": 0},
        )

        result = response.message.content.strip()

        if result not in {"0", "1", "2"}:
            raise ValueError(
                f"Gemma returned an invalid classification for article {identifier}: "
                f"{result!r}"
            )

        con.execute(
            "UPDATE Article SET gemmaClassification = ? WHERE Id = ?",
            (int(result), article_id),
        )
        con.commit()
        print(f"Saved classification for {identifier}: {result}")

    print("Unloading Gemma")
    ollama.generate(model=MODELS["gemma"], keep_alive=0)
    print("Gemma classification complete")

def run_llama():
    pass

def run_phi():
    pass

if __name__ == "__main__":
    main()
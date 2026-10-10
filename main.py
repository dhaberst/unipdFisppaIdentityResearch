import sys
from pathlib import Path

import ollama

FOLDER = Path("rawTXTArticles")
MODEL = "gemma4:12b"

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "Summarize this article."

    for path in sorted(FOLDER.glob("*.txt")):
        text = path.read_text(encoding="utf-8")

        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": f"{query}\n\n---\n\n{text}"}],
            options={"num_ctx": 16384, "temperature": 0},
        )

        print(f"\n===== {path.name} =====")
        print(response.message.content)

    ollama.generate(model=MODEL, keep_alive=0)


if __name__ == "__main__":
    main()
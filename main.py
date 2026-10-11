import sys
from pathlib import Path

import ollama

FOLDER = Path("rawTXTArticles")
MODELS = {
    "gemma": "gemma4:12b",
    "llama": "llama3.1:8b",
    "phi": "phi4",
}

def main():
    run_gemma()
    run_llama()
    run_phi()

def run_gemma():
    query = sys.argv[1] if len(sys.argv) > 1 else "Summarize this article."

    for path in sorted(FOLDER.glob("*.txt")):
        text = path.read_text(encoding="utf-8")

        response = ollama.chat(
            model=MODELS["gemma"],
            messages=[{"role": "user", "content": f"{query}\n\n---\n\n{text}"}],
            options={"num_ctx": 16384, "temperature": 0},
        )

        print(f"\n===== {path.name} =====")
        print(response.message.content)

    ollama.generate(model=MODELS["gemma"], keep_alive=0)

def run_llama():
    pass

def run_phi():
    pass

if __name__ == "__main__":
    main()
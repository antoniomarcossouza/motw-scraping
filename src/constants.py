from pathlib import Path

DATA_DIR = (Path() / "data").resolve()
DATA_DIR.mkdir(exist_ok=True, parents=True)

PAGES_DIR = (DATA_DIR / "original" / "pages").resolve()
PAGES_DIR.mkdir(exist_ok=True, parents=True)

BOOKS_DIR = (DATA_DIR / "original" / "books").resolve()
BOOKS_DIR.mkdir(exist_ok=True, parents=True)


AAC_FILE = Path(Path() / "data" / "aac.jsonl")

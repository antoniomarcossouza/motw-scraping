import json
from pathlib import Path

from motw import (
    MemoryOfTheWorldAPI,
)

DATA_DIR = (Path() / "data").resolve()
DATA_DIR.mkdir(exist_ok=True, parents=True)


def main():
    motw = MemoryOfTheWorldAPI()
    for page in range(1, 2):
        pages_dir = DATA_DIR / "original" / "pages"
        pages_dir.mkdir(exist_ok=True, parents=True)
        page_file = pages_dir / f"page_{page}.json"

        if page_file.is_file():
            return

        page_content = motw.get_page_data(page)
        page_file.write_text(json.dumps(page_content, indent=4))

        book_ids = {item["_id"] for item in page_content["_items"]}
        books_dir = DATA_DIR / "original" / "books"
        books_dir.mkdir(exist_ok=True, parents=True)
        for book_id in book_ids:
            book_file = books_dir / f"{book_id}.json"
            book_content = motw.get_book_details(book_id)
            book_file.write_text(json.dumps(book_content, indent=4))

        print(f"Page {page} done.")


if __name__ == "__main__":
    main()

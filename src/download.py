import json

from constants import BOOKS_DIR, PAGES_DIR
from motw import (
    MemoryOfTheWorldAPI,
)


def main():
    motw = MemoryOfTheWorldAPI()
    for page in range(1, motw.last_page + 1):

        page_file = PAGES_DIR / f"page_{page}.json"

        # HACK: Skip existing pages while i debug the script
        if page_file.is_file():
            continue

        page_content = motw.get_page_data(page)
        page_file.write_text(json.dumps(page_content, indent=4))

        book_ids = {item["_id"] for item in page_content["_items"]}

        for book_id in book_ids:
            book_file = BOOKS_DIR / f"{book_id}.json"
            book_content = motw.get_book_details(book_id)
            book_file.write_text(json.dumps(book_content, indent=4))

        print(f"Page {page} done.")


if __name__ == "__main__":
    main()

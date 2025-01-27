import json
from concurrent.futures import ThreadPoolExecutor

from constants import BOOKS_DIR, PAGES_DIR
from motw import MemoryOfTheWorldAPI


def process_page(motw: MemoryOfTheWorldAPI, page: int) -> list | None:
    page_file = PAGES_DIR / f"page_{page}.json"

    # HACK: Skip existing pages
    if page_file.is_file():
        return

    page_content = motw.get_page_data(page)
    page_file.write_text(json.dumps(page_content, indent=4))

    book_ids = {item["_id"] for item in page_content["_items"]}
    return book_ids


def process_book(motw: MemoryOfTheWorldAPI, book_id: str):
    book_file = BOOKS_DIR / f"{book_id}.json"
    book_content = motw.get_book_details(book_id)
    book_file.write_text(json.dumps(book_content, indent=4))


def main():
    motw = MemoryOfTheWorldAPI()

    with ThreadPoolExecutor() as executor:
        future_to_page = {
            executor.submit(process_page, motw, page): page
            for page in range(1, motw.last_page + 1)
        }

        for future in future_to_page:
            book_ids = future.result()
            if book_ids:
                executor.map(
                    lambda book_id: process_book(motw, book_id), book_ids
                )


if __name__ == "__main__":
    main()

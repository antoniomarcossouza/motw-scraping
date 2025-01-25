from datetime import datetime
from pathlib import Path

import pandas as pd

from motw import (
    MemoryOfTheWorldAPI,
    save_csv,
    transform_book_data,
    transform_page_data,
)

DATA_DIR = (Path() / "data").resolve()
DATA_DIR.mkdir(exist_ok=True, parents=True)


def main():
    motw = MemoryOfTheWorldAPI()
    current_date = datetime.now()
    for page in range(1, 2):
        page_content = motw.get_page_data(page)
        page_content_df = pd.DataFrame(
            [
                {
                    "page": page,
                    "response": page_content,
                    "timestamp": current_date,
                }
            ]
        )
        save_csv(page_content_df, DATA_DIR / "response.csv")

        page_items = [
            transform_page_data(data=item, page=page)
            for item in page_content["_items"]
        ]
        page_items_df = pd.DataFrame.from_records(page_items)
        save_csv(page_items_df, DATA_DIR / "items.csv")

        books = [
            transform_book_data(motw.get_book_details(book["id"]))
            for book in page_items
        ]
        books_df = pd.DataFrame.from_records(books)
        save_csv(books_df, DATA_DIR / "books.csv")

        print(f"Page {page} done.")


if __name__ == "__main__":
    main()

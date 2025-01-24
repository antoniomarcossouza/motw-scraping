import time
from datetime import datetime
from pathlib import Path
from pprint import pprint

import pandas as pd

from motw import MemoryOfTheWorldAPI, save_csv, transform_data

DATA_DIR = (Path() / "data").resolve()


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
            transform_data(data=item, page=page)
            for item in page_content["_items"]
        ]
        page_items_df = pd.DataFrame.from_records(page_items)
        save_csv(page_items_df, DATA_DIR / "items.csv")

        pprint(motw.get_book_details(page_items[0]["id"]))

        time.sleep(1.5)


if __name__ == "__main__":
    main()

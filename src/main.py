from datetime import datetime
from pathlib import Path
from pprint import pprint

import pandas as pd

from motw import MemoryOfTheWorldAPI, save_csv, transform_data

DATA_DIR = (Path() / "data").resolve()


def main():
    motw = MemoryOfTheWorldAPI()
    current_date = datetime.now()
    for i in range(1, 2):
        page_content = motw.get_page_data(i)
        page_content_df = pd.DataFrame(
            [{"page": i, "response": page_content, "timestamp": current_date}]
        )
        save_csv(page_content_df, DATA_DIR / "response.csv")

        page_items = page_content["_items"]
        pprint(
            [transform_data(item) for item in page_items][0]
        )


if __name__ == "__main__":
    main()

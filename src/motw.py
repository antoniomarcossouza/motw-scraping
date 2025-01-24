from pathlib import Path

import httpx
import pandas as pd


class MemoryOfTheWorldAPI:
    def __init__(self):
        self.url = "https://books.memoryoftheworld.org/books"
        self.last_page = int(
            (
                httpx.get(f"{self.url}?page=1")
                .json()["_links"]["last"]["href"]
                .split("=")[-1]
            )
        )

    def get_page_data(self, page: int):
        return httpx.get(f"{self.url}?page={page}").json()


def save_csv(df: pd.DataFrame, path: Path):
    if path.is_file():
        df.to_csv(path_or_buf=path, index=False, header=False, mode="a")
    else:
        df.to_csv(path_or_buf=path, index=False, header=True, mode="w")


def transform_data(data: dict):
    return data

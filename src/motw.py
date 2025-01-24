from pathlib import Path

import httpx
import pandas as pd
from urllib.parse import quote_plus


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
    def transform_format(fmt: dict):
        fmt["url"] = (
            f"{data['library_url']}{fmt.pop('dir_path')}{fmt.pop('file_name')}"
        )
        return fmt

    data["id"] = data.pop("_id")
    data["library_url"] = f'https:{data["library_url"]}'
    data["cover_url"] = f"{data['library_url']}{data['cover_url']}"
    data["formats"] = [transform_format(fmt) for fmt in data["formats"]]
    return data

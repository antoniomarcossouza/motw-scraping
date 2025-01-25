from pathlib import Path

import httpx
import pandas as pd


class MemoryOfTheWorldAPI:
    def __init__(self):
        self.last_page = int(
            (
                httpx.get("https://books.memoryoftheworld.org/books?page=1")
                .json()["_links"]["last"]["href"]
                .split("=")[-1]
            )
        )

    def get_page_data(self, page: int):
        return httpx.get(
            f"https://books.memoryoftheworld.org/books?page={page}"
        ).json()

    def get_book_details(self, book_id: str):
        return httpx.get(
            f"https://library.memoryoftheworld.org/book/{book_id}"
        ).json()


def save_csv(df: pd.DataFrame, path: Path):
    if path.is_file():
        df.to_csv(path_or_buf=path, index=False, header=False, mode="a")
    else:
        df.to_csv(path_or_buf=path, index=False, header=True, mode="w")


def transform_page_data(data: dict, page: int):
    def transform_format(fmt: dict):
        fmt["url"] = (
            f"{data['library_url']}{fmt.pop('dir_path')}{fmt.pop('file_name')}"
        )
        return fmt

    data["page"] = page
    data["id"] = data.pop("_id")
    data["library_url"] = f'https:{data["library_url"]}'
    data["cover_url"] = f"{data['library_url']}{data['cover_url']}"
    data["formats"] = [transform_format(fmt) for fmt in data["formats"]]
    return data


def transform_book_data(data: dict):
    data["id"] = data.pop("_id")
    cleaned_abstract = data["abstract"].replace("\n", "  ")
    data["abstract"] = cleaned_abstract
    return data

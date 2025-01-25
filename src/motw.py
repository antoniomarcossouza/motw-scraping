
import httpx


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

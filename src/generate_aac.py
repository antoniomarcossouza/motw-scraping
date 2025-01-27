import json

from constants import AAC_FILE, BOOKS_DIR


def transform_book_data(data: dict):
    data["book_id"] = data.pop("_id")
    data["description"] = data.pop("abstract")
    del data["title_sort"]
    data["library_url"] = f"https:{data['library_url']}"
    data["cover_url"] = f"{data['library_url']}{data['cover_url']}"
    for fmt in data["formats"]:
        fmt["url"] = (
            f"{data['library_url']}{fmt['dir_path']}{fmt['file_name']}"
        )
        del fmt["dir_path"]
        del fmt["file_name"]

    return data


def main():

    lines = (
        transform_book_data(json.load(book_file.open()))
        for book_file in BOOKS_DIR.glob("*.json")
    )

    with AAC_FILE.open("a") as aac_f:
        for line in lines:
            aac_f.write(json.dumps(line))
            aac_f.write("\n")


if __name__ == "__main__":
    main()

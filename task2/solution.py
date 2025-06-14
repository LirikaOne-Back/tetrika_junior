import csv
import requests
from bs4 import BeautifulSoup

BASE = "https://ru.wikipedia.org"


def get_letters():
    url = f"{BASE}/wiki/Категория:Животные_по_алфавиту"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    sub = soup.find("div", id="mw-subcategories")
    letters = {}
    if not sub:
        return letters

    for a in sub.find_all("a"):
        txt = a.text.strip()
        if txt.startswith("Животные на "):
            letter = txt.split("Животные на ")[1]
            href = a["href"]
            letters[letter] = BASE + href
    return letters


def count_category(cat_url: str) -> int:
    count = 0
    url = cat_url

    while True:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        pages = soup.find("div", id="mw-pages")
        if not pages:
            break

        for ul in pages.find_all("ul"):
            count += len(ul.find_all("li"))

        nxt = pages.find("a", string="Следующая страница")
        if nxt and nxt.get("href"):
            url = BASE + nxt["href"]
        else:
            break

    return count


def main():
    letters = get_letters()
    alphabet = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

    with open("beasts.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for L in alphabet:
            if L in letters:
                n = count_category(letters[L])
                w.writerow([L, n])


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import csv


def parse_animals(site: str, url: str) -> dict:
    animal_counts = {}
    next_url = url
    marker_for_stop = False

    while next_url:
        html_doc = requests.get(next_url).text

        soup = BeautifulSoup(html_doc, 'html.parser')
        category_groups = soup.find_all("div", class_="mw-category-group")

        for group in category_groups:
            a_all = group.find_all('a')

            for link in a_all:
                if link.get('href', '') and link.text not in ("Знаменитые животные по алфавиту", "Породы по алфавиту"):
                    if link.text[0] > "Z":  # TODO Если нужны только русскоязычные названия. Если нужны и англоязычные - заменить эту строку на ту, что ниже...
                    # if link.text[0] >= "A":
                        animal_counts[link.text[0]] = animal_counts.get(link.text[0], 0) + 1
                    else:
                        marker_for_stop = True
                        break

            if marker_for_stop:
                break

        if marker_for_stop:
            break

        next_url = soup.find("a", string="Следующая страница")

        if next_url:
            href = next_url.get('href')
            next_url = site + href

    return animal_counts


if __name__ == "__main__":
    result = parse_animals("https://ru.wikipedia.org",
                           "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83")

    with open('beasts.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)

        for letter in sorted(result.keys()):
            writer.writerow([letter, result[letter]])

import json
from pathlib import Path

from bs4 import BeautifulSoup

from genshin.download.main import html_dir

json_dir = Path.cwd() / "json_data"


def write_json(obj, file_name: str):
    with open(json_dir / file_name, "w") as file:
        json.dump(obj, file, ensure_ascii=False, indent=2)


def parse_html_to_json(html_filename: str):
    with open(html_dir / html_filename, "r") as file:
        content = file.read()
    soup = BeautifulSoup(content, "lxml")
    tables = soup.select("table.sortable.wikitable")
    characters_list_table: BeautifulSoup = tables[0]
    characters_list = []
    for tr in characters_list_table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        stars = int(tds[0].contents[0].attrs["alt"].split(" ")[0])
        name = tds[2].text.strip()
        gods_eye = tds[3].text.strip()
        weapon = tds[4].text.strip()
        sex = tds[5].text.strip()
        area = tds[6].text.strip()
        character = {
            "stars": stars,
            "name": name,
            "gods_eye": gods_eye,
            "weapon": weapon,
            "sex": sex,
            "area": area,
        }
        characters_list.append(character)
        print(stars, name, gods_eye, weapon, sex, area)
    json_file_name = html_filename.replace(".html", ".json")
    write_json(characters_list, json_file_name)


if __name__ == '__main__':
    html_file = "genshin_1.html"
    parse_html_to_json(html_file)

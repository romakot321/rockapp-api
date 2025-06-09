import asyncio
import os
import aiohttp
import pathlib
from bs4 import BeautifulSoup
from models import Rock
from scraper import get_page
import json

base_url = "https://mindat.org"
API_URL = os.getenv("API_URL", "http://localhost:8000")
FROM_PAGE = int(os.getenv("FROM_PAGE", "0"))
TO_PAGE = int(os.getenv("TO_PAGE", 55000))
WORKERS_COUNT = 20
rocks = {}


def parse_mineral_page(html: str, page_id: int) -> Rock | None:
    global rocks

    if "Illegal Page" in html:
        return

    soup = BeautifulSoup(html, "html.parser")
    data = {}

    image_part = soup.find_all("div", {"class": "userbigpicture noborder"})
    if image_part:
        image = image_part[0].find("img")
        if image and "src" in image.attrs:
            data["image_url"] = base_url + "/" + str(image.attrs["src"]).lstrip("/")

    name_part = soup.find("h1", {"class": "mineralheading"})
    name = name_part.text.strip()

    if page_id in rocks.keys():
        rock = rocks[page_id]
        rock.name = name.lower()
        return rock

    synonyms = []
    synonyms_table = soup.find("div", {"class": "newgrouptable3"})
    if synonyms_table is not None:
        for synonym in synonyms_table.find_all("a"):
            synonyms.append(synonym.text)
    data["synonyms"] = synonyms

    parent_part = soup.find_all("div", {"id": "mhenttype"})
    if parent_part:
        parent_name_part = parent_part[0].find("a")
        if parent_name_part:
            data["parent"] = parent_name_part.text

    about = {}
    phys_prop = {}
    geological = {}
    other = {}
    locations = []
    description = ""

    for column in soup.find("div", {"id": "introdata"}).find_all("div", recursive=False):
        span = column.find("span")
        if span is None:
            continue
        key = span.text.strip(":").lower()

        div = column.find("div", recursive=False)
        if div is None:
            continue
        value = div.text
        about[key] = value

    description_part = soup.find("div", {"class": "padder4 lineandahalf"})
    description = description_part.text.strip()

    for i in soup.find_all("h2", {"class": "nogloss mindatadivh2"}):
        if "Physical Properties of " + name in i.text:
            physical_properties_part = i.find_next_sibling("div", {"class": "collapsesection"})
            for column in physical_properties_part.find_all("div", {"class": "mindatarow"}, recursive=False):
                key = column.find("div", {"class": "mindatath"}).text.strip(":").lower()
                value = column.find("div", {"class": "mindatam2"}).text
                phys_prop[key] = value
        elif "Geological Environment" in i.text:
            geological_part = i.find_next_sibling("div", {"class": "collapsesection"})
            for column in geological_part.find_all("div", {"class": "mindatarow"}):
                if "Geological Setting:" not in column.text:
                    continue
                geological["fracture"] = column.find("div", {"class": "mindatam2"}).text
        elif "Other Information" in i.text:
            other_part = i.find_next_sibling("div", {"class": "collapsesection"})
            for column in other_part.find_all("div", {"class": "mindatarow"}):
                if "Health Risks:" not in column.text:
                    continue
                other["danger"] = column.find("div", {"class": "mindatam2"}).text
        elif "Locality List" in i.text:
            localities_part = i.find_next_sibling("div", {"class": "collapsesection"})
            localities_part = localities_part.find("table", {"class": "loclisttable"})
            for country in localities_part.find_all("td", {"class": "country"}):
                locations.append(country.find("div").text)

    for k, v in about.items():
        data[k] = v
    for k, v in phys_prop.items():
        data[k] = v
    for k, v in geological.items():
        data[k] = v.lower()
    for k, v in other.items():
        data[k] = v.lower()
    data["description"] = description
    data["locations"] = locations
    data["name"] = name.lower()

    return Rock(**data)


def get_mineral_page(page_id: int) -> str:
    if pathlib.Path(f"cache/min-{page_id}.html").exists():
        with open(f"cache/min-{page_id}.html", "r") as f:
            return f.read()

    content = get_page(base_url + f"/min-{page_id}.html")

    with open(f"cache/min-{page_id}.html", "w") as f:
        f.write(content)
    return content


async def send_rock(rock: Rock):
    async with aiohttp.ClientSession(base_url=API_URL) as session:
        while True:
            try:
                resp = await session.post("/api/rock", json=rock.model_dump(mode="json"), headers={"rock-storage-token": "iloverocks"})
            except Exception as e:
                print(e)
                continue
            if resp.status == 201:
                break
    print(f"Sended {rock.name}")


async def get_page(page_id) -> str | None:
    i = 0
    while True:
        page = get_mineral_page(page_id)
        if "Just a moment..." not in page:
            break
        await asyncio.sleep(5)
        i += 1
        if i >= 5:
            return None
    return page


async def run(from_page, to_page):
    global rocks
    for page_id in range(from_page, to_page):
        print("Trying page " + str(page_id))
        page = await get_page(page_id)
        if page is None:
            print(f"Failed to get page {page_id}")
            continue
        print("Get page " + str(page_id))
        try:
            rock = parse_mineral_page(page, page_id)
        except Exception as e:
            print(f"ERROR ON PAGE {page_id}", str(e))
            continue
        if rock is None:
            continue
        for synonym_id in rock.synonyms:
            rocks[synonym_id] = rock
        rocks[page_id] = rock
        print(rock)
        await send_rock(rock)
        await asyncio.sleep(1)


async def main():
    page_step = (TO_PAGE - FROM_PAGE) // WORKERS_COUNT
    tasks = []
    for from_page in range(FROM_PAGE, TO_PAGE, page_step):
        tasks.append(asyncio.create_task(run(from_page, from_page + page_step)))
    await asyncio.gather(*tasks)
    print("Instance finished")


asyncio.run(main())

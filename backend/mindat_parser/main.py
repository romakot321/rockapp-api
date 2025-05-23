import asyncio
import os
import aiohttp
import pathlib
from bs4 import BeautifulSoup
from models import Rock
import json

base_url = "https://mindat.org"
API_URL = os.getenv("API_URL", "http://localhost:8000")
rocks = {}


def parse_mineral_page(html: str, page_id: int) -> Rock | None:
    global rocks

    if "Illegal Page" in html:
        return

    soup = BeautifulSoup(html, "html.parser")

    name_part = soup.find("h1", {"class": "mineralheading"})
    name = name_part.text.strip()
    data = {}

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


async def get_mineral_page(page_id: int) -> str:
    if pathlib.Path(f"cache/min-{page_id}.html").exists():
        with open(f"cache/min-{page_id}.html", "r") as f:
            return f.read()

    async with aiohttp.ClientSession(base_url=base_url) as session:
        resp = await session.get(
            f"min-{page_id}.html",
            cookies={"guestid": "189726597", "mindat": "pu4uo62odo792elvh1ueo38gia"},
            headers={
                "Host": "www.mindat.org",
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            },
        )
        assert resp.status == 200, await resp.text()

        content = await resp.text()
        with open(f"cache/min-{page_id}.html", "w") as f:
            f.write(content)
        return content


async def send_rock(rock: Rock):
    async with aiohttp.ClientSession(base_url=API_URL) as session:
        resp = await session.post("/api/rock", json=rock.model_dump(mode="json"), headers={"rock-storage-token": "iloverocks"})
        assert resp.status == 201, await resp.text()


async def main():
    global rocks
    for page_id in range(1, 50):
        page = await get_mineral_page(page_id)
        rock = parse_mineral_page(page, page_id)
        if rock is None:
            continue
        for synonym_id in rock.synonyms:
            rocks[synonym_id] = rock
        rocks[page_id] = rock
        print(rock)
        await send_rock(rock)
        await asyncio.sleep(3)


asyncio.run(main())

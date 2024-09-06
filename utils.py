import os
import json
import requests
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

proxies = {"http": os.environ.get("PROXY_URL"), "https": os.environ.get("PROXY_URL")}


def initial_load_data():
    with open("data/product.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    docs = []
    for row in tqdm(data, total=len(data)):
        content = _load_content(row)
        if content:
            row["content"] = content
            docs.append(row)
    return docs


@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def make_request(url, proxies):
    try:
        response = requests.get(url, proxies=proxies)
    except requests.exceptions.SSLError:
        response = requests.get(url, proxies=proxies, verify=False)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response


def _load_content(row):
    url, produkt = row["url"], row["produkt"]
    if produkt == "Indikator":
        return _load_indicator(url)
    elif produkt in [
        "Faltblatt",
        "Webtabelle",
        "Tabellenband",
        "Applikation",
        "Infografik",
        "Basler Atlas",
        "Dashboard",
    ]:
        unterthema = row["unterthema"] if row["unterthema"] else ""
        return " \n ".join(
            [row["bezeichnung"], row["thema"], unterthema, row["beschreibung"]]
        )
    elif produkt in ["Dossier-Artikel", "Bericht/Analyse"]:
        volltext = row["ergebnis_volltext"] if row["ergebnis_volltext"] else ""
        unterthema = row["unterthema"] if row["unterthema"] else ""
        return " \n ".join(
            [
                row["bezeichnung"],
                row["thema"],
                unterthema,
                row["beschreibung"],
                volltext
            ]
        )
    elif produkt == "Webartikel":
        return _load_webartikel(url)


def _load_indicator(url: str) -> str:
    id = url.split("&id=")[1]
    metadata_url = f"https://statabs.github.io/indikatoren/metadata/single/{id}.json"
    response = make_request(metadata_url, proxies)
    if response:
        data = response.json()
        return " \n ".join(
            [data["title"], data["subtitle"], data["lesehilfe"], data["erlaeuterungen"]]
        )
    return None


def _load_webartikel(url: str) -> str:
    response = make_request(url, proxies)
    text = None
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        page_div = soup.find("div", class_="page")
        if page_div:
            target_tags = page_div.find_all(["h1", "h2", "p"])
            text = " \n ".join([tag.get_text(strip=True) for tag in target_tags])
    return text


if __name__ == "__main__":
    data = initial_load_data()
    with open("data/product_enriched.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from pathlib import Path

main_content_id = "paddingLR12"
test_law = "https://www.gesetze-im-internet.de/estg/__18.html"

law_base_fmt = "https://www.gesetze-im-internet.de/estg/__{paragraph}.html"
law_paragraph_max = 19

CACHE_PATH = Path(".lawcache")


@dataclass
class LawConfig:
    cache_path: Path
    config_path: Path
    law_url_fmt: str
    law_max_paragraph: int


@dataclass
class LawHeader:
    law: str
    paragraph: int


@dataclass
class LawContent:
    absaetze: list


@dataclass
class Law:
    header: LawHeader


def get_paragraph(paragraph: int, config: LawConfig) -> str:
    """
    Check if the paragraph has already been downloaded. I fit is not cached, fetch it from remote
    """
    if paragraph > config.law_max_paragraph:
        print(f"[-] error: {paragraph} > {config.law_max_paragraph}")
        return None

    if not config.cache_path.exists():
        print(f"[*] cache not present yet. creating at {config.cache_path}")
        config.cache_path.mkdir(exist_ok=False)

    paragraph_path = config.cache_path / f"{paragraph}.html"
    if paragraph_path.exists():
        print("[*] law locally found. getting from cache")
        with open(paragraph_path, "r") as f:
            return f.read()
    else:
        # fetchthe new website and cache it
        fetch_url = config.law_url_fmt.format(paragraph=paragraph)
        print(f"[*] law locally not found. fetching {fetch_url}")
        r = requests.get(fetch_url)

        if r.status_code != 200:
            print("[-] err gettings website")
            return None

        print(f"[*] caching file to {paragraph_path}")
        with open(paragraph_path, "w") as f:
            f.write(r.text)

        return r.text


def parse_block(html_doc: str) -> Law:
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_content = soup.find(id=main_content_id)

    title = soup.find("div", class_="jnheader").h1

    print(title)
    print(title.string)
    print(title.span)
    print(title.span.string)

    header: LawHeader = LawHeader(title.string, title.span.string)

    return Law(header)


def main():
    config: LawConfig = LawConfig(CACHE_PATH, ".", law_base_fmt, 19)
    p = get_paragraph(18, config)
    law = parse_block(p)
    # r = requests.get(test_law)
    # law = parse_block(r.text)
    print(law)


if __name__ == "__main__":
    main()

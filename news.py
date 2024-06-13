import asyncio
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup as Soup

tags = {
    "Карьера": "https://vc.ru/hr",
    "Разработка": "https://vc.ru/dev",
    "Будущее": "https://vc.ru/future",
    "Техника": "https://vc.ru/tech",
    "Медиа": "https://vc.ru/media",
    "Маркетинг": "https://vc.ru/marketing",
    "SEO": "https://vc.ru/seo",
    "Дизайн": "https://vc.ru/design",
}
DEFAULT_TEXT = "Заглушка для сайта представляет собой отдельную страницу, показывающуюся " \
               "пользователю в случаях, когда основной контент ресурса недоступен."


def replace(text: str):
    return " ".join(filter(lambda sym: bool(sym), text.replace("\n", "", text.count("\n")).split()))


async def retrieve_json(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            _json = await response.json()
            data = _json.get("data", {})
            next_url = url + f"/more?last_id={data['last_id']}&last_sorting_value={data['last_sorting_value']}"
            soup = Soup(data.get("items_html", ""), "html.parser")

            return next_url, soup


async def retrieve_html(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return Soup(text, "html.parser")


async def get_news_by_tag(link: str, next_page: str = None, n: int = 0) -> dict:
    news = {}
    if n > 2:
        return news
    if link is not None:
        try:
            html = await asyncio.create_task(retrieve_html(link))
        except AttributeError as error:
            return await get_news_by_tag(link, next_page, n + 1)
        news["data"] = parse_news(html)
        return news


def parse_news(soup: Soup) -> list:
    values = []
    for new in soup.find_all("div", {"class": "content"}):

        media = new.find("div", {"class": "media"})
        photo = media.find("img") if media is not None else None

        description = new.find_all("div", {"class": "block-wrapper--default"})
        caption = new.find("div", {"class": "content-title"})

        time_values = [int(v if v.isdigit() else 1) for v in new.find("time").text.split(".")[::-1]]
        if len(time_values) != 3:
            time_values = new.find("time").text

        values.append({
            "title": replace(caption.text if caption is not None else ""),
            "description": replace(description[1].text if len(description) > 1 else DEFAULT_TEXT),
            "link": "https://vc.ru" + new.find("a", {"class": "content__link"}).get("href"),
            "image": photo.get("src") if photo is not None else None,
            "date": datetime(*time_values) if isinstance(time_values, list) else time_values,
            "author": replace(new.find("div", {"class": "author__main"}).text)
        })
    return values


async def retrieve_data(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    soup = Soup(text, "html.parser")

    media = soup.find("div", {"class": "media"})
    photo = media.find("img") if media is not None else None

    text = "<br><br>".join([
        replace(p.text) for p in soup.find_all("div", {"class": "block-wrapper__content"})
    ])

    time_values = [int(v if v.isdigit() else 1) for v in soup.find("time").text.split(".")[::-1]]
    if len(time_values) != 3:
        time_values = soup.find("time").text

    return {
        "title": replace(soup.find("h1", {"class": "content-title"}).text),
        "text": text,
        "date": datetime(*time_values) if isinstance(time_values, list) else time_values,
        "author": replace(soup.find("div", {"class": "author__main"}).text),
        "image": photo.get("src") if photo is not None else None,
    }


async def get_new_by_link(link: str, n: int = 0) -> dict:
    if n > 2:
        return {}
    try:
        return await asyncio.create_task(retrieve_data(link))
    except Exception as error:
        return await asyncio.create_task(get_new_by_link(link, n + 1))

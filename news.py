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
            soup = Soup(text, "html.parser")
            feed = soup.find("div", {"class": "feed"})
            next_url = url + f"/more?last_id={feed.get('data-feed-last-id')}&" \
                               f"last_sorting_value={feed.get('data-feed-last-sorting-value')}"
            return next_url, soup


async def get_news_by_tag(link: str, next_page: str = None, n: int = 0) -> dict:
    news = {}
    if n > 2:
        return news
    if link is not None:
        try:
            if next_page is not None:
                next_page, html = await asyncio.create_task(retrieve_json(next_page))
            else:
                next_page, html = await asyncio.create_task(retrieve_html(link))
        except AttributeError:
            return await get_news_by_tag(link, next_page, n + 1)
        news["data"], news["next_page"] = parse_news(html), next_page
        return news


def parse_news(soup: Soup) -> list:
    values = []
    for new in soup.find_all("div", {"class": "feed__item"}):
        feed = new.find("div", {"class": "content-feed"})

        photo = new.find("div", {"class": "l-island-c"})
        photo = photo.find("div", {"class": "andropov_image"}) if photo is not None else None
        content = new.find("div", {"class": "content-container"})
        description = content.find_all("div", {"class": "l-island-a"})
        caption = new.find("div", {"class": "content-title"})

        num_date = int(new.find("time").get("data-date"))
        values.append({
            "title": replace(caption.text if caption is not None else ""),
            "description": replace(description[1].text if len(description) > 1 else DEFAULT_TEXT),
            "link": new.find("a", {"class": "content-header__item"}).get("href"),
            "image": photo.get("data-image-src") if photo is not None else None,
            "id": feed.get("data-content-id"),
            "date": datetime.fromtimestamp(num_date).strftime("%d.%m.%Y"),
            "author": replace(new.find("div", {"class": "content-header-author__name"}).text)
        })
    return values


async def retrieve_data(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

    soup = Soup(text, "html.parser")

    content = soup.find("div", {"class": "content"})
    text = "<br><br>".join([
        replace(p.text) for p in content.find_all("div", {"class": "l-island-a"})
    ][:-1])

    num_date = int(soup.find("time").get("data-date"))

    photo = soup.find("div", {"class": "l-island-c"})
    photo = photo.find("div", {"class": "andropov_image"}) if photo is not None else None

    return {
        "title": replace(soup.find("h1", {"class": "content-title"}).text),
        "text": text,
        "date": datetime.fromtimestamp(num_date).strftime("%d.%m.%Y"),
        "author": replace(soup.find("div", {"class": "content-header-author__name"}).text),
        "image": photo.get("data-image-src") if photo is not None else None,
    }


async def get_new_by_link(link: str, n: int = 0) -> dict:
    if n > 2:
        return {}
    try:
        return await asyncio.create_task(retrieve_data(link))
    except Exception as error:
        return asyncio.run(get_new_by_link(link, n + 1))

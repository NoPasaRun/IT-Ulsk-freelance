import asyncio
import json
import math
import os
import random
from collections import OrderedDict
from typing import List

from flask import Flask, render_template, request, session, redirect, Blueprint
from pathlib import Path

from db import Session
from models import Company, Rating, Events

from news import tags, get_news_by_tag, get_new_by_link


def create_app(static_dir: Path, templates_dir: Path):
    flask_app = Flask(
        __name__,
        static_folder=static_dir,
        template_folder=templates_dir
    )
    flask_app.register_blueprint(router)

    return flask_app


router = Blueprint("router", __name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True


COMPANIES_PER_PAGE = 4
RATINGS_PER_PAGE = 15


def create_pagination(params: str, current_page: int, total_pages: int, route: str) -> list:
    index = current_page - 2 if current_page - 2 > 1 else 2
    pagination = [
        {"text": 1, "link": f"/{route}?page=1&{params}"},
        *[
            {"text": index, "link": f"/{route}?page={index}&{params}"}
            for index in range(index, index + 5 if index + 5 < total_pages else total_pages)
        ],
        {"text": total_pages, "link": f"/{route}?page={total_pages}&{params}"}
    ]
    if current_page - 1 > 3:
        pagination[1]["text"] = "..."
    if total_pages - current_page > 3:
        pagination[-2]["text"] = "..."
    return pagination[:total_pages]


@app.get('/')
@router.get("/")
def about():
    return render_template('about.html')


@app.get('/news')
@router.get('/news')
def news():
    if not (link := tags.get(request.args.get("theme"))):
        link = random.choice(list(tags.values()))
    data = asyncio.run(get_news_by_tag(link))
    session["next_page"], session["link"] = data.get("next_page"), link

    queryset = data.get("data")

    return render_template(
        'news.html', top=queryset[:3], queryset=queryset[3:]
    )


@app.post('/news')
@router.post('/news')
def news_more():
    if not (session.get("next_page") and session.get("link")):
        return redirect("/news")
    data = asyncio.run(get_news_by_tag(session["link"], session["next_page"]))
    session["next_page"] = data.get("next_page")

    return json.dumps(data)


@app.get("/news-detail")
@router.get("/news-detail")
def news_detail():
    link = request.args.get("link")
    if link is None:
        return redirect("/news")
    data = asyncio.run(get_new_by_link(link))

    random_link = random.choice(list(tags.values()))
    random_data = asyncio.run(get_news_by_tag(random_link))

    return render_template("news-detail.html", main_new=data, queryset=random_data["data"])


@app.get("/companies")
@router.get("/companies")
def companies():
    params = request.args

    data = {
        "name": params.get("name"),
        "offer": params.get("offer"),
        "technology": params.get("technology")
    }
    with Session() as ses:
        queryset = Company.all(ses, **data)
    new_params = "&".join([f"{k}={v}" for k, v in data.items() if v is not None])

    pages = math.ceil(len(queryset) / COMPANIES_PER_PAGE)
    current = int(params.get("page", 1))

    queryset = queryset[(current-1)*COMPANIES_PER_PAGE:current*COMPANIES_PER_PAGE]
    return render_template(
        "company.html",
        queryset=queryset,
        prev_link=(f"/companies?page={current - 1}&{new_params}" if current > 1 else None),
        next_link=(f"/companies?page={current + 1}&{new_params}" if current < pages else None),
        pagination=create_pagination(new_params, current, pages, "companies")
    )


@app.get("/ratings")
@router.get("/ratings")
def ratings():
    params = request.args
    with Session() as ses:
        queryset = Rating.all(ses)

    pages = math.ceil(len(queryset) / RATINGS_PER_PAGE)
    current = int(params.get("page", 1))

    queryset = queryset[(current-1)*RATINGS_PER_PAGE:current*RATINGS_PER_PAGE]
    return render_template(
        "ratings.html",
        queryset=queryset,
        prev_link=(f"/ratings?page={current - 1}" if current > 1 else None),
        next_link=(f"/ratings?page={current + 1}" if current < pages else None),
        pagination=create_pagination("", current, pages, "ratings")
    )


@app.get("/company-detail/<int:company_id>")
@router.get("/company-detail/<int:company_id>")
def company_detail(company_id: int):
    with Session() as ses:
        company = Company.get(ses, company_id)
    if company is not None:
        return render_template("company-detail.html", company=company)
    return redirect("/companies")


@app.get("/eco-system")
@router.get("/eco-system")
def eco_system():
    with Session() as ses:
        events = Events.all(ses)
    return render_template("eco-system.html", queryset=events)


@app.get("/event-detail/<int:event_id>")
@router.get("/event-detail/<int:event_id>")
def event_detail(event_id: int):
    with Session() as ses:
        event = Events.get(ses, event_id)
    if event is not None:
        return render_template("event-detail.html", event=event)
    return redirect("/eco-system")


def generate_distribution(queryset: List, attr_name: str, limit: int = 5):
    values = {"total": 0, "data": OrderedDict(), "amount": limit}
    for item in queryset:
        for attr_val in getattr(item, attr_name, []):
            values["data"][attr_val] = values["data"].get(attr_val, 0) + 1
    values["total"] = total = sum(values["data"].values())
    values["data"] = {
        key: values["data"][key]
        for key in sorted(values["data"], key=values["data"].get)[-limit:]
    }
    values["data"]["Other"] = total - sum(values["data"].values())
    return values


def generate_histogram_y(queryset: List, limit: int = 7):
    max_val = round(queryset[0].income / 10 ** 6, 2)
    min_val = round(queryset[-1].income / 10 ** 6, 2)

    add = (max_val - min_val) // limit
    values = [min_val, *[min_val + add * i for i in range(1, limit - 1)], max_val]

    return list(map(
        lambda val: f"{val} млн" if val < 1000 else f"{round(val / 1000, 2)} млрд", values
    ))


def generate_histogram_x(queryset: List):
    max_val = max(queryset, key=lambda item: item.income)
    return list(map(
        lambda item: {
            "title": item.name,
            "procent": item.income / max_val.income
        }, queryset
    ))


@app.get("/dashboard/")
@router.get("/dashboard/")
def dashboard():
    with Session() as ses:
        queryset = Company.all(ses, name="", offer="", technology="")

    tech_dist = generate_distribution(queryset, "technologies")
    offer_dist = generate_distribution(queryset, "offers")

    histogram_queryset = sorted(queryset, key=lambda item: item.income)[-10:]
    hist_y = generate_histogram_y(histogram_queryset)
    hist_x = generate_histogram_x(histogram_queryset)

    date_y = [f"{num} ч" for num in [20, 30, 50, 80, 100, 150, 180][::-1]]
    date_x = [
        {"title": title, "procent": value / 180}
        for title, value in zip(
            ['янв', 'фев', 'мар', 'апр', 'май', 'июнь', 'июль', 'авг', 'сен', 'окт', 'ноя', 'дек'],
            [180, 80, 160, 120, 80, 120, 160, 30, 100, 75, 150, 75]
        )
    ]

    profession_data = {"Data Science - 450 в.": 35, "DevOps - 320 в.": 20,
                       "Web Development - 100 в.": 10, "AI/ML - 50 в.": 20,
                       "Mobile Development - 30 в.": 15}
    country_data = {"Россия": 5, "Украина": 3, "Беларусь": 6, "Молдавия": 9, "Азербайджан": 2}
    page_data = {"Рейтинги": 9, "Новости": 11, "ИТ-компании": 5, "Экосистема региона": 3, "Дашборды": 7}

    return render_template(
        "dashboard.html",
        tech_dist=tech_dist,
        offer_dist=offer_dist,
        hist_y=hist_y, hist_x=hist_x,
        country_data={"total": sum(country_data.values()), "data": country_data, "amount": len(country_data)},
        page_data={"total": sum(page_data.values()), "data": page_data, "amount": len(page_data)},
        date_y=date_y, date_x=date_x,
        profession_data={
            "total": sum(profession_data.values()), "data": profession_data, "amount": len(profession_data)
        },
    )


if __name__ == '__main__':
    ...

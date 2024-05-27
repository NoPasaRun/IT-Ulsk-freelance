import os
from datetime import datetime, date
from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models

from config import root


class Company(models.Model):
    name: str = models.CharField(verbose_name="Company name", max_length=64)
    image_link: str = models.CharField(verbose_name="Image link", max_length=64)
    income: int = models.BigIntegerField(verbose_name="Income", default=0)
    quantity: int = models.SmallIntegerField(verbose_name="Quantity", default=0)
    creation_date: date = models.DateField(verbose_name="Creation date", default=date.today)
    growth: float = models.DecimalField(verbose_name="Growth rate", decimal_places=3, default=0, max_digits=4)
    offers: list = ArrayField(models.CharField(null=True, blank=True), verbose_name="Offers", default=list)
    technologies: list = ArrayField(models.CharField(null=True, blank=True), verbose_name="Technologies", default=list)
    business_number: str = models.CharField(verbose_name="Business number", max_length=16)
    address: str = models.CharField(verbose_name="Address", max_length=128)
    leader_info: str = models.CharField(verbose_name="Leader info", max_length=64)
    description: str = models.TextField(verbose_name="Description", default="", null=True, blank=True)
    contact_info: str = models.CharField(verbose_name="Contact info", max_length=64)
    web_site_link: str = models.CharField(verbose_name="Website link", max_length=64)
    vk_link: str = models.CharField(verbose_name="VK link", max_length=64, null=True, blank=True)
    tg_link: str = models.CharField(verbose_name="TG link", max_length=64, null=True, blank=True)

    @property
    def is_phone(self):
        return all([not sym.isalpha() for sym in self.contact_info])

    @property
    def age(self) -> float:
        now = datetime.now()
        delta = now - self.creation_date
        return round(delta.year + delta.day / 365, 2)

    class Meta:
        db_table = 'company'


class Rating(models.Model):

    name: str = models.CharField(verbose_name="Company name", max_length=32)
    income: str = models.CharField(verbose_name="Income", max_length=16, null=True, blank=True)
    growth: str = models.CharField(verbose_name="Growth rate", max_length=8, null=True, blank=True)

    class Meta:
        db_table = 'ratings'


class Events(models.Model):

    title: str = models.CharField(verbose_name="Event title", max_length=32)
    caption: str = models.CharField(verbose_name="Caption", max_length=128, null=True, blank=True)
    short_description: str = models.CharField(verbose_name="Short description", max_length=256, null=True, blank=True)
    description: str = models.TextField(verbose_name="Description", default="", null=True, blank=True)
    facts: list = ArrayField(models.CharField(null=True, blank=True), verbose_name="Facts", default=list)
    tg_link: str = models.CharField(verbose_name="TG link", max_length=128, null=True, blank=True)
    vk_link: str = models.CharField(verbose_name="VK link", max_length=128, null=True, blank=True)
    site_link: str = models.CharField(verbose_name="Website link", max_length=128, null=True, blank=True)
    image_dir: str = models.CharField(verbose_name="Image dir", max_length=128)
    image_link: str = models.CharField(verbose_name="Image link", max_length=128)

    @property
    def image_urls(self) -> List[str]:
        path = str(os.path.join(root, *self.image_dir.split('/')))
        return [str(os.path.join(self.image_dir, filename)) for filename in os.listdir(path)]

    class Meta:
        db_table = 'events'

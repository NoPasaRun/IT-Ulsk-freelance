import os
from datetime import date, datetime

from typing import List

from sqlalchemy import select, String, BigInteger, SmallInteger, Date, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.dialects.postgresql import ARRAY

from settings import root
from db import Session, engine


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)

    @classmethod
    def get(cls, session: Session, _id: int) -> 'Base':
        result = session.execute(select(cls).where(cls.id == _id))

        return result.scalar()

    @classmethod
    def count(cls, session: Session) -> int:
        return session.query(cls).count()

    @classmethod
    def all(cls, session: Session) -> List['Base']:
        output = session.execute(select(cls))
        return [row[0] for row in output.fetchall()]


class Company(Base):
    __tablename__ = 'company'

    name: Mapped[str] = mapped_column(String(64))
    image_link: Mapped[str] = mapped_column(String(64))
    income: Mapped[int] = mapped_column(BigInteger())
    quantity: Mapped[int] = mapped_column(SmallInteger())
    creation_date: Mapped[date] = mapped_column(Date())
    growth: Mapped[float] = mapped_column(Numeric())
    offers: Mapped[list] = mapped_column(ARRAY(String))
    technologies: Mapped[list] = mapped_column(ARRAY(String))
    business_number: Mapped[str] = mapped_column(String(16))
    address: Mapped[str] = mapped_column(String(128))
    leader_info: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    contact_info: Mapped[str] = mapped_column(String(64))
    web_site_link: Mapped[str] = mapped_column(String(64))
    vk_link: Mapped[str] = mapped_column(String(64), nullable=True)
    tg_link: Mapped[str] = mapped_column(String(64), nullable=True)

    @classmethod
    def all(cls, session: Session, name: str, offer: str, technology: str) -> List['Company']:
        filters = filter(lambda val: val is not None,
             [
                 cls.name.like(f'%{name}%') if name else None,
                 cls.offers.contains([offer]) if offer else None,
                 cls.technologies.contains([technology]) if technology else None
             ]
        )
        output = session.execute(select(cls).where(*filters))
        return [row[0] for row in output.fetchall()]

    @property
    def is_phone(self):
        return all([not sym.isalpha() for sym in self.contact_info])

    @property
    def age(self) -> float:
        now = datetime.now()
        delta = now - self.creation_date
        return round(delta.year + delta.day / 365, 2)


class Rating(Base):
    __tablename__ = 'ratings'

    name: Mapped[str] = mapped_column(String(32))
    income: Mapped[str] = mapped_column(String(16), nullable=True)
    growth: Mapped[str] = mapped_column(String(8), nullable=True)


class Events(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(32))
    caption: Mapped[str] = mapped_column(String(128), nullable=True)
    short_description: Mapped[str] = mapped_column(String(256), nullable=True)
    description: Mapped[str] = mapped_column(String(4096), nullable=True)
    facts: Mapped[list] = mapped_column(ARRAY(String))
    tg_link: Mapped[str] = mapped_column(String(128), nullable=True)
    vk_link: Mapped[str] = mapped_column(String(128), nullable=True)
    site_link: Mapped[str] = mapped_column(String(128), nullable=True)
    image_dir: Mapped[str] = mapped_column(String(128))
    image_link: Mapped[str] = mapped_column(String(128))

    @property
    def image_urls(self) -> List[str]:
        path = str(os.path.join(root, *self.image_dir.split('/')))
        return [str(os.path.join(self.image_dir, filename)) for filename in os.listdir(path)]


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

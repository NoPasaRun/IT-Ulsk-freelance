from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import db_url


engine = create_engine(url=db_url, echo=True)
Session = sessionmaker(bind=engine)

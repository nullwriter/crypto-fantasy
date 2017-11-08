from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BOT_ENGINE = create_engine('sqlite:///cryptofantasy.sqlite3', echo=False)
BOT_ORM_SESSION = sessionmaker(bind=BOT_ENGINE)

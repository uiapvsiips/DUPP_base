#создать engine с параметрами и sessionmaker
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import sync_db_url

engine = create_engine(sync_db_url, connect_args={"options": "-c timezone=utc-2"})

Session = sessionmaker(engine)




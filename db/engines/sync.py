#создать engine с параметрами и sessionmaker
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_url

engine = create_engine(db_url, connect_args={"options": "-c timezone=utc-2"})

Session = sessionmaker(engine)




#создать engine с параметрами и sessionmaker
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg2://stas:stas01@localhost:5432/uppdb', connect_args={"options": "-c timezone=utc-2"})

Session = sessionmaker(engine)





# engine =  URL   ./clothes.db
# session = to write queries to the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "sqlite:///./clothes.py"

engine = create_engine(url=DATABASE_URL,connect_args={"check_same_thread":False})

sessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



